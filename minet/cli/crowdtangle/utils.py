# =============================================================================
# Minet CrowdTangle CLI Utils
# =============================================================================
#
# Miscellaneous generic functions used throughout the CrowdTangle actions.
#
import csv
import sys
import casanova
import ndjson
from tqdm import tqdm

from minet.utils import prettyprint_seconds
from minet.cli.utils import print_err, die
from minet.crowdtangle import CrowdTangleAPIClient
from minet.crowdtangle.exceptions import (
    CrowdTangleInvalidTokenError,
    CrowdTangleRateLimitExceeded,
    CrowdTangleInvalidJSONError
)


def make_paginated_action(method_name, item_name, csv_headers, get_args=None,
                          announce=None):

    def action(cli_args, output_file):

        # Do we need to resume?
        need_to_resume = False

        if getattr(cli_args, 'resume', False):
            need_to_resume = True

            if cli_args.output is None:
                die(
                    'Cannot --resume without knowing the output (use -o/--output rather stdout).',
                )

            if cli_args.sort_by != 'date':
                die('Cannot --resume if --sort_by is not `date`.')

            if cli_args.format != 'csv':
                die('Cannot --resume jsonl format yet.')

            with open(cli_args.output, 'r', encoding='utf-8') as f:
                resume_reader = casanova.reader(f)

                last_cell = None
                resume_loader = tqdm(desc='Resuming', unit=' lines')

                for cell in resume_reader.cells('datetime'):
                    resume_loader.update()
                    last_cell = cell

                resume_loader.close()

                if last_cell is not None:
                    last_date = last_cell.replace(' ', 'T')
                    cli_args.end_date = last_date

                    print_err('Resuming from: %s' % last_date)

        if callable(announce):
            print_err(announce(cli_args))

        # Loading bar
        loading_bar = tqdm(
            desc='Fetching %s' % item_name,
            dynamic_ncols=True,
            unit=' %s' % item_name,
            total=cli_args.limit
        )

        if cli_args.format == 'csv':
            writer = csv.writer(output_file)

            if not need_to_resume:
                writer.writerow(csv_headers(cli_args) if callable(csv_headers) else csv_headers)
        else:
            writer = ndjson.writer(output_file)

        client = CrowdTangleAPIClient(cli_args.token, rate_limit=cli_args.rate_limit)

        args = []

        if callable(get_args):
            args = get_args(cli_args)

        def before_sleep(retry_state):
            exc = retry_state.outcome.exception()

            if isinstance(exc, CrowdTangleRateLimitExceeded):
                reason = 'Call failed because of rate limit!'

            elif isinstance(exc, CrowdTangleInvalidJSONError):
                reason = 'Call failed because of invalid JSON payload!'

            else:
                reason = 'Call failed because of server timeout!'

            tqdm.write(
                '%s\nWill wait for %s before attempting again.' % (
                    reason,
                    prettyprint_seconds(retry_state.idle_for, granularity=2)
                ),
                file=sys.stderr
            )

        create_iterator = getattr(client, method_name)
        iterator = create_iterator(
            *args,
            partition_strategy=getattr(cli_args, 'partition_strategy', None),
            limit=cli_args.limit,
            format='csv_row' if cli_args.format == 'csv' else 'raw',
            per_call=True,
            detailed=True,
            namespace=cli_args,
            before_sleep=before_sleep
        )

        try:
            for details, items in iterator:
                if details is not None:
                    loading_bar.set_postfix(**details)

                for item in items:
                    writer.writerow(item)

                loading_bar.update(len(items))

        except CrowdTangleInvalidTokenError:
            loading_bar.close()
            die([
                'Your API token is invalid.',
                'Check that you indicated a valid one using the `--token` argument.'
            ])

        loading_bar.close()

    return action
