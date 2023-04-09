import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.oauth2_invalidate_token.post_oauth2_invalidate_token import (
    PostOauth2InvalidateTokenResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauth2InvalidateToken:
    @pytest.mark.skip(reason="上手く invalidation できない理由を要調査。")
    def test_post_oauth2_invalidate_token(
        self, real_oauth2_app_client: TwitterApiRealClient
    ):
        expected_response = PostOauth2InvalidateTokenResponseBody(
            access_token=(
                real_oauth2_app_client._real_request_client._auth.token["access_token"]
                # pyright: reportOptionalSubscript=false
                # pyright: reportOptionalMemberAccess=false
            ),
        )

        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key=os.environ["API_KEY"],
                api_secret=os.environ["API_SECRET"],
                query={"access_token": expected_response.access_token},
            )
        )

        print(real_response.json())
        print(expected_response.json())

        assert real_response == expected_response


class TestMockPostOauth2InvalidateToken:
    def test_mock_post_oauth2_invalidate_token(
        self, mock_oauth2_app_client: TwitterApiMockClient
    ):
        expected_response = PostOauth2InvalidateTokenResponseBody(access_token="")

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/oauth2/invalidate_token",
                expected_response,
            )
            .request("https://api.twitter.com/oauth2/invalidate_token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query={"access_token": "DUMMY_ACCESS_TOKEN"},
            )
        ) == expected_response