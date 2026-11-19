

from typing import Any

import httpx
from schemas import YoutubeUploadsExtractor


class YoutubeDataExtractor:
    def __init__(self, api_key: str | None = None):

        self.api_key = api_key
        self.uploads_id = None

    def get_channel_uploads_playlist_id(self, handle: str) -> None | str:

        if not self.api_key:
            return None

        url: str = "https://youtube.googleapis.com/youtube/v3/channels"

        # need to refactor to make in pydantic
        params: dict[str, str] = {
            "part": "contentDetails",
            "forHandle": handle,
            "key": self.api_key,
        }
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)  # need decoupling after

                response.raise_for_status()

                data: dict[str, Any] = response.json()

                return YoutubeUploadsExtractor.model_validate(data).uploads

        except httpx.HTTPStatusError as e:
            raise e  # f"HTTP error : {e.response.status_code} - {e.response.text}"

        except httpx.RequestError as e:
            raise e  # f"Network error : {e}"

        return None
