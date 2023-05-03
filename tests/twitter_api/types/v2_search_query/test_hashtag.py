from twitter_api.types.v2_search_query.hashtag import Hashtag
from twitter_api.types.v2_search_query.search_query import SearchQuery


class TestHashtag:
    def test_hashtag(self):
        assert str(Hashtag("Twitter")) == "#Twitter"

    def test_hashtag_with_mark(self):
        assert str(Hashtag("#Twitter")) == "#Twitter"

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.hashtag("Twitter"))) == "#Twitter"
