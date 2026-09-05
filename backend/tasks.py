from celery import Celery
from detection import detect_spill
from models import db, Incident
import os

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def process_image(filepath):
    with open(filepath, 'rb') as f:
        image_bytes = f.read()
    result = detect_spill(image_bytes)
    # save to DB
    incident = Incident(...)
    db.session.add(incident)
    db.session.commit()
    return incident.id