### This project was stopped for uncertain period.

### Description

Imagine if you want to subsribe not to youtube channel for all the videos author creates, but only some of them. This bot will (try to) solve this problem. You can send link to youtube channel and then keyword or regex, and if video with such pattern appears on channel, it will send you a link. Expected stack of technologies: aiogram, postgresql, celery (for updating last videos), docker, google api client.

### Done

Add subscription

Show all subscriptions

Create dp.py

Create api_requests.py

### Work Plan

Update subscription

Delete subscription

Background tasks

Send menu keyboard

Add help command

### db format

1. Users' tables: name - username, fields: id, channel_name, channel_id, pattern
2. Table 'channels': fields: channel_id, video_0, video_1, video_2, video_3, video_4

youtube api allows 100 search requests per day

[link to youtube api docs](https://developers.google.com/youtube/v3/docs/search/list)

[link to corey tutorial](https://www.youtube.com/watch?v=th5_9woFJmk)
