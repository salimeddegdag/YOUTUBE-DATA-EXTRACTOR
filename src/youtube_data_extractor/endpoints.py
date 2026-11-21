from pydantic import BaseModel, Field

CHANNELS_URL = "https://youtube.googleapis.com/youtube/v3/channels"

class ChannelQueryParams(BaseModel):
    
    part : str = "contentDetails"
    for_handle : str = Field(min_length=1,serialization_alias="forHandle")
    api_key : str = Field(min_length=1,serialization_alias="key")

    def to_query_params(self) -> dict[str,str]:
        return self.model_dump(by_alias=True,exclude_none=True)
    
    