import click

from src.main import get_users_feeds_from_follow_events_and_tweets_files


@click.group()
@click.option('--tweets-file', help='Path for file containing tweets.')
@click.option('--follow-events-file', help='Path for file containing follow events.')
@click.pass_context
def cli(ctx, tweets_file, follow_events_file):
    ctx.ensure_object(dict)
    ctx.obj['tweets_file'] = tweets_file
    ctx.obj['follow_events_file'] = follow_events_file


@click.command()
@click.pass_context
def print_users_feeds(ctx):
    follow_events_file_path = ctx.obj['follow_events_file']
    tweets_file_path = ctx.obj['tweets_file']
    output = get_users_feeds_from_follow_events_and_tweets_files(
        follow_events_file_path,
        tweets_file_path,
    )
    for line in output:
        print(line)


cli.add_command(print_users_feeds)


if __name__ == '__main__':
    cli()
