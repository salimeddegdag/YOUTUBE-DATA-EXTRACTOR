from pydantic import BaseModel, ConfigDict, Field, field_validator

CHANNELS_URL: str = "https://youtube.googleapis.com/youtube/v3/channels"
PLAYLIST_ITEMS_URL: str = "https://youtube.googleapis.com/youtube/v3/playlistItems"
VIDEO_DATA_URL: str = "https://youtube.googleapis.com/youtube/v3/videos"

MAX_VIDEO_IDS_PER_REQUEST: int = 50


# ==============================================================================
# Enpoint 1 - Query Params: from handle to channel_id
# ==============================================================================
class ChannelQueryParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    part: str = "contentDetails"
    for_handle: str = Field(min_length=1, serialization_alias="forHandle")
    api_key: str = Field(min_length=1, serialization_alias="key")

    #! Need to add validation for the for_handle and api_key to handle special cases


# ==============================================================================
# Enpoint 2 - Query Params: from channel_id to videos_id
# ==============================================================================
class PlaylistItemsQueryParms(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    part: str = "contentDetails"
    playlist_id: str = Field(min_length=1, serialization_alias="playlistId")
    max_results: int = Field(ge=1, le=50, serialization_alias="maxResults", default=50)
    next_page_token: str | None = Field(default=None, serialization_alias="pageToken")
    api_key: str = Field(min_length=1, serialization_alias="key")


# ==============================================================================
# Enpoint 3 - Query Params: from videos_id to videos_data
# ==============================================================================


class VideoDataQueryPrams(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    part: str = "snippet,statistics,contentDetails"
    api_key: str = Field(min_length=1, serialization_alias="key")
    videos_ids: str = Field(min_length=1, default=list, serialization_alias="id")
    next_page_token: str | None = Field(default=None, serialization_alias="pageToken")

    @field_validator("videos_ids", mode="before")
    @classmethod
    def join_if_from_list(cls, videos_id_list: list[str]):
        return ",".join(video_id for video_id in videos_id_list if video_id)
