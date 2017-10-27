from sched import scheduler
from datetime import datetime


@scheduler.scheduled_job('cron', day_of_week='mon-fri', second="*/5")
def morning():
    print("Holis! I am a task at {}".format(datetime.now()))