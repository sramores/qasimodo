from pymitter import EventEmitter
from os.path import dirname, basename, isfile
import glob


event_controller = EventEmitter()

modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

