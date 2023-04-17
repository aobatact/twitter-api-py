"""
OAuth 2.0 を用いたユーザ認証のフローを説明するサンプル。

refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
"""

import os
import sys
from textwrap import dedent

from twitter_api.api.types.v2_oauth2.twitter_oauth2_access_token_client import (
    TwitterOAuth2AccessTokenClient,
)
from twitter_api.api.types.v2_scope import ALL_SCOPES
from twitter_api.client import TwitterApiClient
from twitter_api.error import TwitterApiError

YOUR_CALLBACK_URL = os.environ["CALLBACK_URL"]

try:
    # Backend: 認証用の URL を作成します。
    backend = (
        TwitterApiClient.from_oauth2_user_flow_env(
            callback_url=YOUR_CALLBACK_URL,
            scope=ALL_SCOPES,
        )
        .request("https://twitter.com/i/oauth2/authorize")
        .generate_authorization_url()
    )

    # ユーザに認証ページへの URL を返却します。
    user = backend

    # Frontend: ユーザは承認ボタンを押した後、リダイレクトした CallbackURL をバックエンドに返します。
    user = user.print_request_url().input_response_url()

    # Backend: アクセストークンを取得し、 Twitter API のクライアントを作成します。
    token = (
        TwitterOAuth2AccessTokenClient.from_authorization_response_url_env(
            callback_url=YOUR_CALLBACK_URL,
            authorization_response_url=user.authorization_response_url,
            code_verifier=backend.code_verifier,
            state=backend.state,
        )
        .request("https://api.twitter.com/2/oauth2/token")
        .post()
    )

    # 認証トークンを取得完了！
    print("\n🌟 Create User OAuth Token!! 🌟\n", file=sys.stderr)
    print(
        dedent(
            f"""
            OAUTH2_USER_ACCESS_TOKEN={token.access_token}
            """
        ).strip()
    )

    # Twitter API を呼ぶことができるようになりました。
    client = TwitterApiClient.from_oauth2_bearer_token(token.access_token)

    tweet = (
        client.chain()
        .request("https://api.twitter.com/2/tweets/:id")
        .get("1460323737035677698")
        .data
    )

except TwitterApiError as error:
    print(error, file=sys.stderr)
