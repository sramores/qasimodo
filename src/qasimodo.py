from threading import Thread
from slackclient import SlackClient
import handlers
import signal
import sys
import os


class Qasimodo(object):
    
    def __init__(self, token):
        self.event_handler = HandlerThread(token)
        
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def start(self):
        self.event_handler.start()
        #self.event_handler.join()

    def stop(self):
        self.event_handler.stop()

class HandlerThread(Thread):

    def __init__(self, token):
        Thread.__init__(self, daemon=True)
        self.__emitter = handlers.event_controller
        self.__continue = True
        self.__token = token

    def run(self):
        try:
            sc = SlackClient(self.__token)
            if sc.rtm_connect():
                while self.__continue:
                    events = sc.rtm_read()
                    for e in events:
                        self.__emitter.emit(e['type'], (e, sc))
            else:
                raise Exception("cannot connect")
        except Exception as ex:
            print(ex)

    def stop(self):
        self.__continue = False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        token = sys.argv[1]
    elif 'BOT_TOKEN' in os.environ:
        token = os.environ['BOT_TOKEN']
    else:
        raise Exception('No token found for the bot')

    qasimodo = Qasimodo(token)
    qasimodo.start()
    qasimodo.event_handler.join()

