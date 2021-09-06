from .celery import app
# from db import get


@app.task
def hello():
    return 'hello world'


@app.task
def update_all():
    """Updates last 5 videos on every channel in db, scheduled every day"""
    pass


@app.task
def send_notification():
    """Send a notification message according to users' subscriptions"""
    pass
