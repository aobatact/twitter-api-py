import os
import sys

from twitter_api.api.types.v2_scope import ALL_SCOPES
from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]

try:
    client = (
        TwitterApiClient.from_oauth2_user_flow_env(
            callback_url=YOUR_CALLBACK_URL,
            scope=[
                "tweet.read",
                "users.read",
            ],
        )
        .resource("https://twitter.com/i/oauth2/authorize")
        .generate_authorization_url()
        .open_request_url()
        .input_response_url()
        .resource("https://api.twitter.com/2/oauth2/token")
        .post()
        .generate_client()
    )

    tweets = (
        client.chain()
        .resource("https://api.twitter.com/2/tweets")
        .get(
            {"ids": ["1460323737035677698"]},
        )
        .data
    )

    print(tweets)


except TwitterApiError as error:
    print(error, file=sys.stderr)
