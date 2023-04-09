import pytest

from tests.conftest import synthetic_monitoring_is_disable
from tests.data import JsonDataLoader
from twitter_api.api.resources.v2_dm_conversations.post_v2_dm_conversations import (
    PostV2DmConversationsResponseBody,
)
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient
from twitter_api.client.twitter_api_real_client import TwitterApiRealClient


@pytest.mark.skipif(**synthetic_monitoring_is_disable())
class TestGetV2UserFollowing:
    @pytest.mark.skip("You do not have permission to DM one or more participants.")
    def test_get_v2_user_following(
        self,
        real_auth1_user_client: TwitterApiRealClient,
    ):
        response = (
            real_auth1_user_client.chain()
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                "2244994945",
                {
                    "conversation_type": "Group",
                    "participant_ids": ["944480690", "906948460078698496"],
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
        )

        print(response.json())

        assert True


class TestMockGetV2UserFollowing:
    @pytest.mark.parametrize(
        "json_filename",
        [
            "post_dm_conversations.json",
        ],
    )
    def test_mock_get_v2_user_following(
        self,
        mock_oauth2_app_client: TwitterApiMockClient,
        json_data_loader: JsonDataLoader,
        json_filename: str,
    ):
        expected_response = PostV2DmConversationsResponseBody.parse_obj(
            json_data_loader.load(json_filename)
        )

        assert (
            mock_oauth2_app_client.chain()
            .inject_post_response_body(
                "https://api.twitter.com/2/dm_conversations",
                expected_response,
            )
            .request("https://api.twitter.com/2/dm_conversations")
            .post(
                "2244994945",
                {
                    "conversation_type": "Group",
                    "participant_ids": ["944480690", "906948460078698496"],
                    "message": {
                        "text": "Hello to you two, this is a new group conversation"
                    },
                },
            )
        ) == expected_response