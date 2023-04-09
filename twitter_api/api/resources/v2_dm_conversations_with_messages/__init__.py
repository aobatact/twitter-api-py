from typing import TypeAlias

from typing_extensions import Literal

from .post_v2_dm_conversations_with_messages import (
    PostV2DmConversationsWithParticipantMessagesResources,
)

V2DmConversationsWithParticipantMessagesUrl: TypeAlias = Literal[
    "https://api.twitter.com/2/dm_conversations/with/:participant_id/messages"
]


class V2DmConversationsWithParticipantMessagesResources(
    PostV2DmConversationsWithParticipantMessagesResources
):
    pass