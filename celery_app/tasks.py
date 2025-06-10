from celery_app.celery_app import app
import subprocess


@app.task
def scrape_and_save():
    subprocess.run(["python", "main.py"])
