from config import YoutubeApiSettings, youtube_api_setting

from extractor import YoutubeDataExtractor


def main() -> str:

    youtube_api_key: str = youtube_api_setting.api_key.get_secret_value()

    youtube_data_extractor: YoutubeDataExtractor = YoutubeDataExtractor(
        api_key=youtube_api_key
    )
    channels_id = youtube_data_extractor.get_channel_uploads_playlist_id(
        handle="MrBeast"
    )
    print(channels_id)

    return "Done"


if __name__ == "__main__":
    main()
    x = {
        "kind": "youtube#channelListResponse",
        "etag": "mky5yfatRnp-E8N9-BwXGY8W8Dk",
        "pageInfo": {"totalResults": 1, "resultsPerPage": 5},
        "items": [
            {
                "kind": "youtube#channel",
                "etag": "-f8h6RTCebSZttPcDz3dTkMV5yo",
                "id": "UCX6OQ3DkcsbYNE6H8uQQuVA",
                "contentDetails": {
                    "relatedPlaylists": {
                        "likes": "",
                        "uploads": "UUX6OQ3DkcsbYNE6H8uQQuVA",
                    }
                },
            }
        ],
    }
