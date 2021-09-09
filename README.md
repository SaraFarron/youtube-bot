### Work Plan

1. Find solution to background tasks (
   [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html), 
   [dramatiq](https://dramatiq.io/),
   [rq](https://python-rq.org/))
2. Create file that works as background task and make api calls on schedule
3. Update main.py, so it launches background tasks and telegram bot
4. [Optional] Redo db.py. One function that gets command and executes sql. Get, update etc. just generate
this commands take sql output
5. Finish keyboards' creation in bot, update and delete should use it
6. Finish commands in bot
7. Add proper logging
8. Add comments and docs
9. Find host

youtube api allows 100 search requests per day

[link to youtube api docs](https://developers.google.com/youtube/v3/docs/search/list)

[link to corey tutorial](https://www.youtube.com/watch?v=th5_9woFJmk)
