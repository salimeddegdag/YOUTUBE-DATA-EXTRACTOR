from typing import Any

import httpx
from endpoints import (
    CHANNELS_URL,
    PLAYLIST_ITEMS_URL,
    VIDEO_DATA_URL,
    ChannelQueryParams,
    PlaylistItemsQueryParms,
    VideoDataQueryPrams,
)
from pydantic import ValidationError
from schemas import (
    PlaylistItemsPageSchema,
    PlaylistItemsVideoSchema,
    YoutubeUploadsExtractor,
    VideoItem,
    VideoItemsPage,
)


class YoutubeDataExtractor:
    def __init__(self, api_key: str | None = None):

        self.api_key = api_key
        # self.uploads_id = None

    def get_channel_uploads_playlist_id(self, handle: str) -> None | str:

        if not self.api_key:
            return None

        query_params: dict[str, str] = ChannelQueryParams(for_handle=handle, api_key=self.api_key).model_dump(
            by_alias=True
        )

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    url=CHANNELS_URL, params=query_params
                )  # need decoupling after in an other class dedicated to monitoring HTTP/rpc... prtocol

                response.raise_for_status()

                return YoutubeUploadsExtractor.model_validate(response.json()).uploads

        except httpx.HTTPStatusError as e:
            raise e  # f"HTTP error : {e.response.status_code} - {e.response.text}"

        except httpx.RequestError as e:
            raise e  # f"Network error : {e}"

        except ValidationError as e:
            print(e)
            return None

        return None

    def get_playlist_items_video_ids(self, playlist_id: str) -> list[str] | None:

        video_ids: list[str] = []
        # next_page_token: str | None = None

        query_params_obj: PlaylistItemsQueryParms = PlaylistItemsQueryParms(
            api_key=self.api_key,
            playlist_id=playlist_id,
        )

        if not self.api_key:
            return None

        try:
            with httpx.Client(timeout=10.0) as client:
                while True:
                    response = client.get(url=PLAYLIST_ITEMS_URL, params=query_params_obj.model_dump(by_alias=True))
                    response.raise_for_status()

                    page: PlaylistItemsPageSchema = PlaylistItemsPageSchema.model_validate(response.json())

                    video_ids.extend(item.video_id for item in page.items)

                    if not page.next_page_token:
                        break
                    query_params_obj.next_page_token = page.next_page_token

            return video_ids
        
        except httpx.HTTPStatusError as e:
            raise e  # f"HTTP error : {e.response.status_code} - {e.response.text}"

        except httpx.RequestError as e:
            raise e  # f"Network error : {e}"

        except ValidationError as e:
            # print(e)
            return None

    def get_video_data(self, videos_ids_list: list[str]):

        videos_data: list[VideoItem] = []

        batch_size: int = 2
        batch_id_generator = (videos_ids_list[i : i + batch_size] for i in range(0, 2, batch_size))

        query_params_obj: VideoDataQueryPrams = VideoDataQueryPrams(api_key=self.api_key)

        for batch_id in batch_id_generator:
            try:
                with httpx.Client(timeout=10.0) as client:
                    query_params_obj.videos_ids = batch_id

                    response = client.get(url=VIDEO_DATA_URL, params=query_params_obj.model_dump(by_alias=True))
                    response.raise_for_status()

                    
                    page = VideoItemsPage.model_validate(response.json())

                    videos_data.extend(page.video_items)

                    if not page.next_page_token:
                        break
                    query_params_obj.next_page_token = page.next_page_token

            except httpx.HTTPStatusError as e:
                raise e  # f"HTTP error : {e.response.status_code} - {e.response.text}"
    
            except httpx.RequestError as e:
                raise e  # f"Network error : {e}"
    
            except ValidationError as e:
                raise e
            return None
