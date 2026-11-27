from pydantic import AliasPath, BaseModel, Field, ConfigDict


# ==============================================================================
# Enpoint 1 - Result extraction: from handle to channel_id
# ==============================================================================
class YoutubeUploadsExtractor(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    uploads: str | None = Field(
        default=None, validation_alias=AliasPath("items", 0, "contentDetails", "relatedPlaylists", "uploads")
    )


# ==============================================================================
# Enpoint 2 - Result Extraction: channel_id to videos_id
# ==============================================================================
class PlaylistItemsVideoSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    video_id: str | None = Field(default=None, validation_alias=AliasPath("contentDetails", "videoId"))


class PlaylistItemsPageSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[PlaylistItemsVideoSchema] = Field(default_factory=list)
    next_page_token: str | None = Field(default=None, validation_alias="nextPageToken")


# ==============================================================================
# Enpoint 3 - Result Extraction: from videos_id to videos_data
# ==============================================================================
class Snippet(BaseModel):
    model_config = ConfigDict(extra="ignore", forbid=True)
    publish_at: str = Field(min_length=1, validation_alias="publishedAt")
    channel_id: str = Field(min_length=1, validation_alias="channelId")
    channel_title: str = Field(min_length=1, validation_alias="channelTitle")


class Statistics(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    view_count: int = Field(ge=0, validation_alias="viewCount")
    like_count: int = Field(ge=0, validation_alias="likeCount")
    favorite_count: int = Field(ge=0, validation_alias="favoriteCount")
    comment_count: int = Field(ge=0, validation_alias="commentCount")


class ContentDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")
    duration: str = Field(min_length=1, validation_alias="duration")


class VideoItem(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    video_id: str = Field(min_length=1, validation_alias="id")
    snippet: Snippet = Field(default=Snippet, validation_alias="snippet")
    statistics: Statistics = Field(default=Statistics, validation_alias="statistics")
    content_details: ContentDetails = Field(default=ContentDetails, validation_alias="contentDetails")

    def to_flat_dict(self) -> dict[str | int]:
        return (
            {"video_id": self.video_id}
            | self.snippet.model_dump()
            | self.statistics.model_dump()
            | self.content_details.model_dump()
        )


class VideoItemsPage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    video_items: list[VideoItem] = Field(default_factory=list, validation_alias="items")
    next_page_token: str | None = Field(default=None, validation_alias="nextPageToken")

    def to_flat_row(self) -> list[dict[str | int]]:
        return [item.to_flat_dict() for item in self.video_items]
