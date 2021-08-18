import unittest
from src.tweets.persistence import (
    parse_tweet_file,
    parse_tweet_line,
    get_reasons_tweet_line_invalid,
)
from src.tweets.lib import (
    get_user_tweet_feed,
    get_reasons_tweet_invalid,
)
from src.tweets.presentation import (
    format_tweet,
    get_user_feed_output,
    get_user_feeds_output,
)


SAMPLE_TWEET_DATA = [
    'Alan> If you have a procedure with 10 parameters, you probably missed some.',
    'Ward> There are only two hard things in Computer Science: cache invalidation, naming things and off-by-1 errors.',
    'Alan> Random numbers should not be generated with a method chosen at random.',
]


SAMPLE_FOLLOW_EVENT_DATA = [
    'Ward follows Alan',
    'Alan follows Martin',
    'Ward follows Martin, Alan',
]


SAMPLE_USER_FOLLOWER_MAPPING = {
    'Ward': ['Alan', 'Martin'],
    'Alan': ['Martin'],
}


SAMPLE_TWEETS = [
    {
        'author': 'Alan',
        'body': 'If you have a procedure with 10 parameters, you probably missed some.',
    },
    {
        'author': 'Ward',
        'body': 'There are only two hard things in Computer Science: cache invalidation, naming things and off-by-1 errors.',
    },
    {
        'author': 'Alan',
        'body': 'Random numbers should not be generated with a method chosen at random.',
    },
]


SAMPLE_TWEET_FILE_PATH = './sample_data/tweets.txt'
SAMPLE_FOLLOW_EVENT_FILE_PATH = './sample_data/events.txt'


class TestTweets(unittest.TestCase):
    def test_get_reasons_tweet_line_invalid_handles_missing_seperator(self):
        invalid_tweet_line = 'Jason :: This is my tweet without the correct separator!'
        reasons_tweet_line_invalid = get_reasons_tweet_line_invalid(invalid_tweet_line)
        assert len(reasons_tweet_line_invalid) == 1
        assert reasons_tweet_line_invalid[0] == "Missing author/body seperator sequence: '> '."

    def test_get_reasons_tweet_invalid_handles_long_tweet(self):
        long_tweet = {
            'author': 'Jason',
            'body': 'hi' * 100,
        }
        reasons_tweet_invalid = get_reasons_tweet_invalid(long_tweet)
        assert len(reasons_tweet_invalid) == 1
        assert reasons_tweet_invalid[0] == 'Tweet length exceeds 140 characters.'

    def test_parse_tweet_line_parses_tweet_line(self):
        parsed_tweet = parse_tweet_line(SAMPLE_TWEET_DATA[0])
        assert parsed_tweet['author'] == 'Alan'
        assert 'If you have' in parsed_tweet['body']

    def test_parse_tweet_file_parses_tweet_file(self):
        parsed_tweets = parse_tweet_file(SAMPLE_TWEET_FILE_PATH)
        assert len(parsed_tweets) == 3
        assert parsed_tweets[0]['author'] == 'Alan'
        assert 'If you have' in parsed_tweets[0]['body']
        assert parsed_tweets[1]['author'] == 'Ward'
        assert 'There are only two' in parsed_tweets[1]['body']
        assert parsed_tweets[2]['author'] == 'Alan'
        assert 'Random numbers should' in parsed_tweets[2]['body']

    def test_get_user_tweet_feed_gets_authors_tweets(self):
        tweets = [
            {'author': 'Alan', 'body': 'some-body'}
        ]
        user_feed = get_user_tweet_feed('Alan', [], tweets)
        assert len(user_feed) == 1
        assert user_feed[0]['author'] == 'Alan'
        assert user_feed[0]['body'] == 'some-body'

    def test_get_user_tweet_feed_excludes_tweets_of_other_authors(self):
        tweets = [
            {'author': 'Alan', 'body': 'some-body'}
        ]
        user_feed = get_user_tweet_feed('Not Alan', [], tweets)
        assert len(user_feed) == 0

    def test_get_user_tweet_feed_includes_tweets_of_followers(self):
        tweets = [
            {'author': 'Alan', 'body': 'some-body'}
        ]
        user_feed = get_user_tweet_feed('Not Alan', ['Alan'], tweets)
        assert len(user_feed) == 1
        assert user_feed[0]['author'] == 'Alan'
        assert user_feed[0]['body'] == 'some-body'

    def test_format_tweet_formats_tweet(self):
        tweet = {
            'author': 'Jason',
            'body': 'some-body'
        }
        formatted_tweet = format_tweet(tweet)
        assert formatted_tweet == f"@{tweet['author']}: {tweet['body']}"

    def test_get_user_feed_output_gets_output(self):
        tweets = [
            {'author': 'Alan', 'body': 'some-body'},
            {'author': 'Alan', 'body': 'some-other-body'},
        ]
        output = get_user_feed_output('Alan', [], tweets)
        assert len(output) == 3
        assert output[0] == 'Alan'
        assert output[1] == '@Alan: some-body'
        assert output[2] == '@Alan: some-other-body'

    def test_get_user_feeds_output_gets_output(self):
        tweets = [
            {'author': 'Alan', 'body': 'some-body'},
            {'author': 'Bill', 'body': 'some-other-body'},
        ]
        output = get_user_feeds_output(['Alan', 'Bill'], {}, tweets)
        assert len(output) == 4
        assert output[0] == 'Alan'
        assert output[1] == '@Alan: some-body'
        assert output[2] == 'Bill'
        assert output[3] == '@Bill: some-other-body'
