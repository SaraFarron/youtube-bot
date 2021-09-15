from googleapiclient.discovery import build
from os import environ


api_key = environ.get('GOOGLE_API')
environ.get("GOOGLE_APPLICATION_CREDENTIALS")


def pull_videos(response: dict):
    """Pulls videos out of response and returns dictionary of them"""

    items = response['items']
    videos = {
        'channel_id': items[0]['snippet']['channelId'],
        'channel_title': items[0]['snippet']['channelTitle'],
        'videos': {}
    }

    for item in items:
        snippet = item['snippet']
        video_id = item['id']['videoId']
        videos['videos'][video_id] = {
            'title': snippet['title'],
            'publication_date': snippet['publishedAt'],
        }

    return videos


def get_last_videos(channel: str, number=10):
    """Returns dict of last number of videos. If number is not provided returns 10"""

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        channelId=channel,
        order='date',
    )
    response = request.execute()
    next_page_token = response['nextPageToken']
    videos = pull_videos(response)

    while len(videos) < number:
        request = youtube.search().list(
            part='snippet',
            channelId=channel,
            order='date',
            pageToken=next_page_token
        )
        response = request.execute()
        try:  # Perhaps error occurs when channel doesn't have more than 5 videos
            next_page_token = response['nextPageToken']
        except KeyError:
            return videos
        videos['videos'] = videos['videos'] | pull_videos(response)['videos']

    return videos


def filter_videos(videos: dict, pattern: str):
    """Returns filtered by title dict of videos"""

    result = {}

    for video, contents in videos.items():
        if pattern in contents['title']:
            result[video] = contents

    # This whole function is unnecessary because python:
    return {k: v for k, v in videos.items() if pattern in v['title']}
