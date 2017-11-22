from threading import Thread
from slackclient import SlackClient
from sched import scheduler
from sched import *
from handlers import *
from time import sleep
import handlers
import signal
import sys
import os
import logging


class Qasimodo(object):
    def __init__(self, token):
        self.scheduler = scheduler
        self.__client = SlackClient(token)
        if not self.__client.rtm_connect():
            msg = "Cannot connect to Slack"
            logging.critical(msg)
            raise Exception(msg)

        self.event_handler = HandlerThread(self.__client)
        self.__init__scheduler()
        signal.signal(signal.SIGINT, self.__stop)
        signal.signal(signal.SIGTERM, self.__stop)

    def __init__scheduler(self):
        for job in self.scheduler.get_jobs():
            job.modify(kwargs={'client': self.__client})

    def start(self):
        logging.info("Bot starting...")
        self.scheduler.start()
        self.event_handler.start()

    def stop(self):
        logging.info("Bot stopping...")
        self.event_handler.stop()
        self.scheduler.shutdown()

    def __stop(self, *args, **kargs):
        self.stop()


class HandlerThread(Thread):
    def __init__(self, sc):
        Thread.__init__(self, daemon=True)
        self.__emitter = handlers.event_controller
        self.__continue = True
        self.__sc = sc

    def run(self):
        while self.__continue:
            try:
                events = self.__sc.rtm_read()
                for e in events:
                    logging.debug(e)
                    if 'type' in e:
                        self.__emitter.emit(e['type'], e, self.__sc)
            except Exception as ex:
                logging.error("Exception: " + str(ex))

    def stop(self):
        self.__continue = False
        logging.info('Handler stopped')


if __name__ == '__main__':
    level = logging.INFO
    if 'LOG_LEVEL' in os.environ:
        if os.environ['LOG_LEVEL'] == 'DEBUG':
            level = logging.DEBUG
        elif os.environ['LOG_LEVEL'] == 'INFO':
            level = logging.INFO
        elif os.environ['LOG_LEVEL'] == 'WARNING':
            level = logging.WARNING

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=level)
    logging.info("log level set to {}".format(level))

    if len(sys.argv) > 1:
        token = sys.argv[1]
    elif 'BOT_TOKEN' in os.environ:
        token = os.environ['BOT_TOKEN']
    else:
        msg = 'No token found for the bot'
        logging.critical(msg)
        raise Exception(msg)

    qasimodo = Qasimodo(token)
    qasimodo.start()

    while True:
        sleep(3600)
    logging.warning("END")
