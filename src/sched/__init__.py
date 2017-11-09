from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone


scheduler = BackgroundScheduler(timezone=timezone('Europe/Madrid'))

from . import morning