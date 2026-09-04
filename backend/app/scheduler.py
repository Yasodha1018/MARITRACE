from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.tasks import scheduled_satellite_monitoring
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    """Start the background scheduler for automated monitoring"""
    scheduler = BackgroundScheduler()
    
    # Run satellite monitoring every 6 hours
    scheduler.add_job(
        scheduled_satellite_monitoring,
        trigger=IntervalTrigger(hours=6),
        id='satellite_monitoring',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started - monitoring every 6 hours")
    return scheduler

# Initialize scheduler on app startup
scheduler = None

def init_scheduler():
    global scheduler
    if not scheduler:
        scheduler = start_scheduler()
    return scheduler