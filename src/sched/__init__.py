from os.path import dirname, basename, isfile
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import glob


job_defaults = {
    'misfire_grace_time': 50
}

scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=timezone('Europe/Madrid'))

modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
