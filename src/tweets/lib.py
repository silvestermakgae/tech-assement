from collections import namedtuple
from src.tweets.exceptions import InvalidTweet


Tweet = namedtuple('Tweet', ['author', 'body'])


def validate_tweet(tweet, meta):
    reasons = get_reasons_tweet_invalid(tweet)
    if reasons:
        raise InvalidTweet(f'{reasons[0]} meta: {str(meta)}')


def get_reasons_tweet_invalid(tweet):
    reasons = []
    if len(tweet['body']) > 140:
        reasons.append(f'Tweet length exceeds 140 characters.')
    return reasons or None


# TODO: Use generator?
# TODO: Rename to filter_tweets?
def get_user_tweet_feed(user, followers, tweets):
    """
    Filter tweets by author and their followers.
    Returns filtered list of tweets.
    """
    feed = []
    for tweet in tweets:
        author = tweet['author']
        if author == user or author in followers:
            feed.append(tweet)
    return feed
