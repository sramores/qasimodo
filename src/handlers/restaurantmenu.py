from . import event_controller as ec
from os import environ
import logging as log
import constants
import requests


WIT_HEADERS = {
    'Accept': 'application/vnd.wit.20141022+json',
    'Authorization': 'Bearer {}'.format(environ['WITAI_QASIMODO_TOKEN'])
}


def __is_asking_for_menu(msg):
    rs = __send_wit_request(msg)
    intents = rs['outcomes'][0]['entities']['intent']
    trait = dict(filter(lambda x: x['value'] == 'restaurant_menu', intents))
    return 'confidence' in trait and trait['confidence'] > 0.7


def __send_wit_request(msg):
    global WIT_HEADERS
    rs = requests.get("https://api.wit.ai/message", {'q': msg}, headers=WIT_HEADERS)
    return rs.json()


def __get_menu():
    return ""


@ec.on("message")
def response(event, client):
    qasimodo_cite = '<@{}>'.format(constants.qasimodo)
    if 'text' in event and (event['text'].stratswith(qasimodo_cite) or event['text'].endswith(qasimodo_cite)):
        msg = event['text'].replace(qasimodo_cite, '')
        if __is_asking_for_menu(msg):
            menu = __get_menu()
            client.rtm_send_message(event['channel'], menu)



