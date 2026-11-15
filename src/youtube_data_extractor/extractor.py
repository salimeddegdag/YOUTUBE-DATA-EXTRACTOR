from typing import Any

import httpx


class YoutubeDataExtractor:
    def __init__(self, api_key: str | None = None):

        self.appi_key = api_key
        self.uploads_id = None

    def get_channel_uploads_playlist_id(self, handle: str) -> None | str:

        if not self.appi_key:
            return None

        url: str = "https://youtube.googleapis.com/youtube/v3/channels"

        # need to refactor to make in pydantic
        params: dict[str, str] = {
            "part": "contentDetails",
            "forHandle": handle,
            "key": self.appi_key,
        }
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)  # need decoupling after

                response.raise_for_status()

                data: dict[str, Any] = response.json()

                if data.get("pageInfo", {}).get("totalResults", 0) == 0:
                    return None

                items: list[Any] = (
                    data.get("items", []) or None
                )  # ! case null and expected list  - (None or [])--> []  weak case of you have a str

                if not items:   # * case of empty list  - not [] --> False  
                    return None

                first_item: any = items[0]

                if not isinstance(first_item,dict):
                    return None

                content_details = first_item.get("contentDetails")

                # if 

                

                # if  response_json_data['pageInfo']['totalResults'] == 0:
                #     return None

                # return response.json()["items"][0]["id"]

        except httpx.HTTPStatusError as e:
            raise e  # f"HTTP error : {e.response.status_code} - {e.response.text}"

        except httpx.RequestError as e:
            raise e  # f"Network error : {e}"

        return None
