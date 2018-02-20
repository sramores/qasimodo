from . import event_controller as ec
from random import random
import logging as log
import constants


TOMATO_RATE = 0.65

@ec.on("message")
def response(event, client):
    if event['user'] == constants.esunol and random() < TOMATO_RATE:
        rs = client.api_call("reactions.add",
                        name='tom',
                        channel=event['channel'],
                        timestamp=event['ts']
                    )

        if 'error' in rs and rs['error']:
            log.warning(rs['error'])
