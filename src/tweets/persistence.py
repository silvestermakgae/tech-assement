from src import utils
from src.tweets.exceptions import InvalidTweetLine


TWEET_LINE_AUTHOR_BODY_SEPERATOR = '> '


def validate_tweet_line(tweet_line, meta):
    reasons = get_reasons_tweet_line_invalid(tweet_line)
    if reasons:
        raise InvalidTweetLine(f'{reasons[0]} meta: {str(meta)}')


def get_reasons_tweet_line_invalid(tweet_line):
    reasons = []
    if TWEET_LINE_AUTHOR_BODY_SEPERATOR not in tweet_line:
        reasons.append(f"Missing author/body seperator sequence: '{TWEET_LINE_AUTHOR_BODY_SEPERATOR}'.")
    return reasons or None


def parse_tweet_line(tweet_line):
    """
    Parses a tweet line into tweet dictionary of author and body.
    Returns a dictionary of tweet author and body.
    """
    author, body = (
        tweet_line
        .split('> ')
    )
    return {
        'author': author,
        'body': body,
    }


# TODO: Use generator?
def parse_tweet_file(path, line_cb=None, tweet_cb=None):
    """
    Parses tweet file into a list of tweet dictionaries.
    Returns list of tweet dictionaries.
    """
    tweets_file = utils.read_text_file(path)
    tweets = []
    for index, line in enumerate(tweets_file):
        meta = {
            'line_number': index + 1,
        }
        if line_cb:
            line_cb(line, meta=meta)
        tweet = parse_tweet_line(line.strip('\n'))
        if tweet_cb:
            tweet_cb(tweet, meta=meta)
        tweets.append(tweet)
    return tweets
