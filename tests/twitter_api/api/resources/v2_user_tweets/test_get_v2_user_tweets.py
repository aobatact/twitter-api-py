import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import json_test_data
from twitter_api.api.resources.v2_user_tweets.get_v2_user_tweets import (
    GetV2UserTweetsResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserTweets:
    def test_get_v2_user_tweets(
        self,
        real_oauth2_app_client: TwitterApiRealClient,
    ):
        response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/2/users/:id/tweets")
            .get("2244994945")
        )

        print(response.json())

        assert get_extra_fields(response) == {}


class TestMockGetV2UserTweets:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_user_tweets_response_default_fields.json",
            "get_v2_user_tweets_response_optional_fields.json",
            "get_v2_user_tweets_response_all_fields.json",
        ],
    )
    def test_mock_get_v2_user_tweets(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_filename: str,
    ):
        response = GetV2UserTweetsResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert get_extra_fields(response) == {}

        assert (
            mock_oauth2_app_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/:id/tweets", response
            )
            .request("https://api.twitter.com/2/users/:id/tweets")
            .get("2244994945")
        ) == response
