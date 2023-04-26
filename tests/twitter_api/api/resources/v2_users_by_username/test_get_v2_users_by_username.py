import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.contexts.spawn_real_client import spawn_real_client
from tests.data import json_test_data
from twitter_api.api.resources.v2_users_by_username.get_v2_users_by_username import (
    GetV2UsersByUsernameResponseBody,
)
from twitter_api.api.types.v2_user.user import User
from twitter_api.client.twitter_api_async_mock_client import TwitterApiAsyncMockClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.types.extra_permissive_model import get_extra_fields


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2User:
    @pytest.mark.parametrize(
        "client_fixture_name,permit",
        [
            ("oauth1_app_real_client", True),
            ("oauth1_user_real_client", True),
            ("oauth2_app_real_client", True),
            ("oauth2_user_real_client", True),
        ],
    )
    def test_get_v2_users_by_username(
        self,
        client_fixture_name: str,
        permit: bool,
        request: pytest.FixtureRequest,
        twitter_dev_user: User,
    ):
        with spawn_real_client(client_fixture_name, request, permit) as real_client:
            response_body = (
                real_client.chain()
                .request("https://api.twitter.com/2/users/by/username/:username")
                .get(twitter_dev_user.username)
            )

            print(response_body.json())

            assert get_extra_fields(response_body) == {}


class TestMockGetV2User:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "get_v2_users_by_username_response_body.json",
        ],
    )
    def test_mock_get_v2_users_by_username(
        self,
        oauth2_app_mock_client: TwitterApiMockClient,
        json_filename: str,
        twitter_dev_user: User,
    ):
        response_body = GetV2UsersByUsernameResponseBody.parse_file(
            json_test_data(json_filename),
        )

        assert get_extra_fields(response_body) == {}

        assert (
            oauth2_app_mock_client.chain()
            .inject_get_response_body(
                "https://api.twitter.com/2/users/by/username/:username", response_body
            )
            .request("https://api.twitter.com/2/users/by/username/:username")
            .get(twitter_dev_user.username)
        ) == response_body


class TestAsyncMockGetV2User:
    @pytest.mark.asyncio
    async def test_async_mock_get_v2_users_by_username(
        self,
        oauth2_app_async_mock_client: TwitterApiAsyncMockClient,
        twitter_dev_user: User,
    ):
        response_body = GetV2UsersByUsernameResponseBody.parse_file(
            json_test_data("get_v2_users_by_username_response_body.json"),
        )

        assert get_extra_fields(response_body) == {}

        assert (
            await (
                oauth2_app_async_mock_client.chain()
                .inject_get_response_body(
                    "https://api.twitter.com/2/users/by/username/:username",
                    response_body,
                )
                .request("https://api.twitter.com/2/users/by/username/:username")
                .get(twitter_dev_user.username)
            )
            == response_body
        )