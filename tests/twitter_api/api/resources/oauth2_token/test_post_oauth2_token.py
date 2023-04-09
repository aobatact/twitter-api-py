import os

import pytest

from tests.conftest import synthetic_monitoring_is_disable
from twitter_api.api.resources.oauth2_token.post_oauth2_token import (
    PostOauth2TokenResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestPostOauth2Token:
    def test_post_oauth2_token(self, real_oauth2_app_client: TwitterApiRealClient):
        expected_response = PostOauth2TokenResponseBody(
            token_type="bearer",
            access_token=(
                real_oauth2_app_client._real_request_client._auth.token["access_token"]
                # pyright: reportOptionalSubscript=false
                # pyright: reportOptionalMemberAccess=false
            ),
        )

        real_response = (
            real_oauth2_app_client.chain()
            .request("https://api.twitter.com/oauth2/token")
            .post(
                api_key=os.environ["API_KEY"],
                api_secret=os.environ["API_SECRET"],
                query={"grant_type": "client_credentials"},
            )
        )

        print(real_response.json())
        print(expected_response.json())

        assert real_response == expected_response


class TestMockPostOauth2Token:
    def test_mock_post_oauth2_token(self, mock_oauth2_app_client: TwitterApiMockClient):
        expected_response = PostOauth2TokenResponseBody(
            token_type="bearer",
            access_token="AAAAAAAAAAAAAAAAAAAAAOeOmQEAAAAAu",
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/oauth2/token",
                expected_response,
            )
            .request("https://api.twitter.com/oauth2/token")
            .post(
                api_key="DUMMY_API_KEY",
                api_secret="DUMMY_API_SECRET",
                query={"grant_type": "client_credentials"},
            )
        ) == expected_response