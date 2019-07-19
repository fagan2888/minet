# =============================================================================
# Minet CrowdTangle CLI Action
# =============================================================================
#
# Logic of the `ct` action.
#
import sys

from minet.cli.utils import DummyTqdmFile, print_err


def crowdtangle_action(namespace):

    # A token is needed to be able to access the API
    if not namespace.token:
        print_err('A token is needed to be able to access CrowdTangle\'s API.')
        print_err('You can provide one using the `--token` argument.')
        sys.exit(1)

    if namespace.output is None:
        output_file = DummyTqdmFile(sys.stdout)
    else:
        output_file = open(namespace.output, 'w')

    if namespace.ct_action == 'posts':
        from minet.cli.crowdtangle.posts import crowdtangle_posts_action

        crowdtangle_posts_action(namespace, output_file)

    elif namespace.ct_action == 'lists':
        from minet.cli.crowdtangle.lists import crowdtangle_lists_action

        crowdtangle_lists_action(namespace, output_file)

    elif namespace.ct_action == 'leaderboard':
        from minet.cli.crowdtangle.leaderboard import crowdtangle_leaderboard_action

        crowdtangle_leaderboard_action(namespace, output_file)

    elif namespace.ct_action == 'search':
        from minet.cli.crowdtangle.search import crowdtangle_search_action

        crowdtangle_search_action(namespace, output_file)

    # Cleanup
    if namespace.output is not None:
        output_file.close()