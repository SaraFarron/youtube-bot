from dramatiq import actor
from api_requests import get_last_videos
from db import get


@actor
def send_notification(link: str, user: str):
    pass  # TODO send message to user with link to new video


@actor
def update_videos(channels: list[str, ]):

    for channel in channels:
        videos = get_last_videos(channel, number=5)

        if videos == get(channel):  # TODO
            continue
        send_notification()
