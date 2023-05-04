from twitter_api.types.v2_search_query.operators.retweet_of_operator import (
    RetweetOfOperator,
)
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestRetweetOfOperator:
    def test_retweet_of_operator(self):
        assert str(RetweetOfOperator("twitterdev")) == "retweets_of:twitterdev"

    def test_query_build(self):
        assert (
            str(SearchQuery.build(lambda q: q.retweet_of("twitterdev")))
            == "retweets_of:twitterdev"
        )
