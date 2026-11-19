from pydantic import AliasPath, BaseModel, Field


class YoutubeUploadsExtractor(BaseModel):
    uploads: str | None = Field(
        default=None,
        validation_alias=AliasPath(
            "items", 0, "contentDetails", "relatedPlaylists", "uploads"
        ),
    )
