from typing import Any
from pydantic import ValidationError

import httpx
from schemas import YoutubeUploadsExtractor

from endpoints import ChannelQueryParams,CHANNELS_URL


class YoutubeDataExtractor:
    def __init__(self, api_key: str | None = None):

        self.api_key = api_key
        self.uploads_id = None

    def get_channel_uploads_playlist_id(self, handle: str) -> None | str:

        if not self.api_key:
            return None

        query_params : dict[str,str] = ChannelQueryParams(
            for_handle=handle,
            api_key=self.api_key).to_query_params()

        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url=CHANNELS_URL, 
                                      params=query_params)  # need decoupling after in an other class dedicated to monitoring HTTP/rpc... prtocol 

                response.raise_for_status()

                data: dict[str, Any] = response.json()

                return YoutubeUploadsExtractor.model_validate(data).uploads
        
        except httpx.HTTPStatusError as e:
            raise e  # f"HTTP error : {e.response.status_code} - {e.response.text}"

        except httpx.RequestError as e:
            raise e  # f"Network error : {e}"

        except ValidationError:
            return None
        
        return None
