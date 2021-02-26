# =============================================================================
# Minet Url Parse CLI Action
# =============================================================================
#
# Logic of the `url-parse` action.
#
import casanova
from ural import (
    is_url,
    is_shortened_url,
    normalize_url,
    get_hostname,
    get_domain_name,
    get_normalized_hostname,
    infer_redirection
)
from tqdm import tqdm

from minet.cli.utils import open_output_file

REPORT_HEADERS = [
    'normalized_url',
    'inferred_redirection',
    'domain_name',
    'hostname',
    'normalized_hostname',
    'probably_shortened'
]


def url_parse_action(namespace):

    output_file = open_output_file(namespace.output)

    enricher = casanova.enricher(
        namespace.file,
        output_file,
        add=REPORT_HEADERS,
        keep=namespace.select
    )

    loading_bar = tqdm(
        desc='Parsing',
        dynamic_ncols=True,
        unit=' rows',
        total=namespace.total
    )

    for row, url in enricher.cells(namespace.column, with_rows=True):
        url = url.strip()

        loading_bar.update()

        if namespace.separator:
            urls = url.split(namespace.separator)
        else:
            urls = [url]

        for url in urls:
            if not is_url(url, allow_spaces_in_path=True):
                enricher.writerow(row)
                continue

            inferred_redirection = infer_redirection(url)

            enricher.writerow(row, [
                normalize_url(
                    url,
                    strip_protocol=namespace.strip_protocol,
                    strip_trailing_slash=True
                ),
                inferred_redirection if inferred_redirection != url else '',
                get_domain_name(url),
                get_hostname(url),
                get_normalized_hostname(url),
                'yes' if is_shortened_url(url) else ''
            ])

    output_file.close()
