from config import YoutubeApiSettings, youtube_api_setting

from extractor import YoutubeDataExtractor


def main() -> str:

    youtube_api_key: str = youtube_api_setting.api_key.get_secret_value()

    youtube_data_extractor: YoutubeDataExtractor = YoutubeDataExtractor(api_key=youtube_api_key)
    channels_id: str = youtube_data_extractor.get_channel_uploads_playlist_id(handle="MrBeast")
    videos_ids: list[str] = youtube_data_extractor.get_playlist_items_video_ids(playlist_id=channels_id)

    video_data = youtube_data_extractor.get_video_data(videos_ids_list=videos_ids)

    # print(video_data)

    return ""


if __name__ == "__main__":
    main()
