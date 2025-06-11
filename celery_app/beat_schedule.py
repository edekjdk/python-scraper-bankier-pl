from datetime import timedelta

beat_schedule = {
    "run-scraper-every-hour": {
        "task": "celery_app.tasks.scrape_and_save",
        "schedule": timedelta(hours=1),
    }
}
