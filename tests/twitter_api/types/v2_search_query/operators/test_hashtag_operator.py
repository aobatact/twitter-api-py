from twitter_api.types.v2_search_query.operators.hashtag_operator import HashtagOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHashtagOperator:
    def test_hashtag_operator(self):
        assert str(HashtagOperator("Twitter")) == "#Twitter"

    def test_hashtag_operator_with_mark(self):
        assert str(HashtagOperator("#Twitter")) == "#Twitter"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.hashtag("Twitter"))) == "#Twitter"
