# =============================================================================
# Minet Youtube CLI Action
# =============================================================================
#
# Logic of the `yt` action.
#
from minet.cli.utils import open_output_file, die


def check_key(cli_args):

    # A key is required to used the API
    if not cli_args.key:
        die([
            'A key is required to access YouTube API.',
            'You can provide it using the --key argument.'
        ])


def youtube_action(cli_args):

    output_file = open_output_file(
        cli_args.output,
        flag='w'
    )

    if cli_args.yt_action == 'videos':
        check_key(cli_args)

        from minet.cli.youtube.videos import videos_action
        videos_action(cli_args, output_file)

    elif cli_args.yt_action == 'comments':
        check_key(cli_args)

        from minet.cli.youtube.comments import comments_action
        comments_action(cli_args, output_file)

    elif cli_args.yt_action == 'captions':
        from minet.cli.youtube.captions import captions_action
        captions_action(cli_args, output_file)

    elif cli_args.yt_action == 'search':
        check_key(cli_args)

        from minet.cli.youtube.search import search_action
        search_action(cli_args, output_file)

    if cli_args.output is not None:
        output_file.close()
