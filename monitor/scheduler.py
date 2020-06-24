from apscheduler.schedulers.background import BackgroundScheduler
from monitor.collector import run_scan


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scan, 'interval', minutes=1)
    scheduler.start()
