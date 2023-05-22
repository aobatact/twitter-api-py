import pytest

from twitter_api.error import SearchQueryDoubleQuotedError
from twitter_api.types.v2_search_query.operators.keyword_operator import KeywordOperator
from twitter_api.types.v2_search_query.operators.operator import CompleteOperator
from twitter_api.types.v2_search_query.search_query import SearchQuery, build


class TestKeywordOperator:
    def test_keyword_operator(self):
        assert str(KeywordOperator("test")) == "test"

    def test_keyword_operator_with_phrase(self):
        assert str(KeywordOperator('"test twitter"')) == '"test twitter"'

    def test_keyword_operator_with_space(self):
        assert str(KeywordOperator("test twitter")) == '"test twitter"'

    def test_keyword_operator_with_emoji(self):
        assert str(KeywordOperator("😃")) == "😃"

    def test_keyword_operator_with_exact_phrase_match(self):
        with pytest.raises(SearchQueryDoubleQuotedError):
            KeywordOperator('"test" twitter')

    def test_query_complete(self):
        assert isinstance(
            build(lambda q: q.keyword("test")),
            CompleteOperator,
        )

    def test_query_build(self):
        assert str(SearchQuery.build(lambda q: q.keyword("test"))) == "test"
