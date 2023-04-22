from functools import partial
from typing import AsyncGenerator, NotRequired, Optional, Self, TypedDict

from pydantic import Field

from twitter_api.api.resources.api_resources import ApiResources
from twitter_api.api.types.v2_expansion import Expansion
from twitter_api.api.types.v2_retweet.retweet import Retweet
from twitter_api.api.types.v2_scope import oauth2_scopes
from twitter_api.api.types.v2_tweet.tweet import Tweet
from twitter_api.api.types.v2_tweet.tweet_field import TweetField
from twitter_api.api.types.v2_tweet.tweet_id import TweetId
from twitter_api.api.types.v2_user.user_field import UserField
from twitter_api.rate_limit.rate_limit_decorator import rate_limit
from twitter_api.types.comma_separatable import CommaSeparatable, comma_separated_str
from twitter_api.types.endpoint import Endpoint
from twitter_api.types.extra_permissive_model import ExtraPermissiveModel
from twitter_api.types.paging import (
    PageResponseBody,
    get_flattend_search_response,
    get_search_response_iter,
)

ENDPOINT = Endpoint("GET", "https://api.twitter.com/2/tweets/:id/retweeted_by")

GetV2TweetRetweetedByQueryParameters = TypedDict(
    "GetV2TweetRetweetedByQueryParameters",
    {
        "expansions": NotRequired[Optional[CommaSeparatable[Expansion]]],
        "max_results": NotRequired[Optional[int]],
        "pagination_token": NotRequired[Optional[str]],
        "tweet.fields": NotRequired[Optional[CommaSeparatable[TweetField]]],
        "user.fields": NotRequired[Optional[CommaSeparatable[UserField]]],
    },
)


def _make_query(query: GetV2TweetRetweetedByQueryParameters) -> dict:
    return {
        "expansions": comma_separated_str(query.get("expansions")),
        "max_results": query.get("expansions"),
        "pagination_token": query.get("expansions"),
        "tweet.fields": comma_separated_str(query.get("tweet.fields")),
        "user.fields": comma_separated_str(query.get("user.fields")),
    }


class GetV2TweetRetweetedByResponseBodyIncludes(ExtraPermissiveModel):
    tweets: list[Tweet] = Field(default_factory=list)

    def extend(self, other: Self) -> None:
        self.tweets.extend(other.tweets)


class GetV2TweetRetweetedByResponseBodyMeta(ExtraPermissiveModel):
    result_count: int
    next_token: Optional[str] = None
    previous_token: Optional[str] = None

    def extend(self, other: Self) -> None:
        self.result_count += other.result_count
        self.next_token = None
        self.previous_token = None


class GetV2TweetRetweetedByResponseBody(ExtraPermissiveModel, PageResponseBody):
    data: list[Retweet] = Field(default_factory=list)
    meta: GetV2TweetRetweetedByResponseBodyMeta
    includes: GetV2TweetRetweetedByResponseBodyIncludes = Field(
        default_factory=GetV2TweetRetweetedByResponseBodyIncludes,
    )
    errors: Optional[list[dict]] = None

    @property
    def meta_next_token(self) -> str | None:
        return self.meta.next_token

    def extend(self, other: Self) -> None:
        self.data.extend(other.data)
        self.meta.extend(other.meta)
        self.includes.extend(other.includes)

        if other.errors is not None:
            if self.errors is not None:
                self.errors.extend(other.errors)
            else:
                self.errors = other.errors


class GetV2TweetRetweetedByResources(ApiResources):
    @oauth2_scopes(
        "tweet.read",
        "users.read",
    )
    @rate_limit(ENDPOINT, "app", requests=75, mins=15)
    @rate_limit(ENDPOINT, "user", requests=75, mins=15)
    def get(
        self, id: TweetId, query: Optional[GetV2TweetRetweetedByQueryParameters] = None
    ) -> GetV2TweetRetweetedByResponseBody:
        """
        リツイートされたツイートの一覧を取得する。

        refer: https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/get-tweets-id-retweeted_by
        """
        return self.request_client.get(
            endpoint=ENDPOINT,
            response_type=GetV2TweetRetweetedByResponseBody,
            url=ENDPOINT.url.replace(":id", id),
            query=_make_query(query) if query is not None else None,
        )


class AsyncGetV2TweetRetweetedByResources(GetV2TweetRetweetedByResources):
    async def get(
        self, id: TweetId, query: Optional[GetV2TweetRetweetedByQueryParameters] = None
    ) -> GetV2TweetRetweetedByResponseBody:
        return super().get(
            id,
            query,
        )

    async def get_iter(
        self, id: TweetId, query: GetV2TweetRetweetedByQueryParameters
    ) -> AsyncGenerator[GetV2TweetRetweetedByResponseBody, None]:
        return get_search_response_iter(partial(self.get, id), query)

    async def get_flattened(
        self, id: TweetId, query: GetV2TweetRetweetedByQueryParameters
    ) -> GetV2TweetRetweetedByResponseBody:
        return await get_flattend_search_response(partial(self.get, id), query)
