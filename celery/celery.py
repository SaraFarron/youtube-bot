from celery import Celery


app = Celery('celery',
             broker='redis://redis:6379/0',
             include=['celery.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
