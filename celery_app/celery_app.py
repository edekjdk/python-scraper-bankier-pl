from celery import Celery


from celery_app.beat_schedule import beat_schedule

app = Celery(
    "scraper",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["celery_app.tasks"],
)

app.conf.beat_schedule = beat_schedule
app.conf.timezone = "Europe/Warsaw"
