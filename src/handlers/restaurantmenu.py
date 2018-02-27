from . import event_controller as ec
from os import environ
from urllib.request import Request, urlopen
from lxml.html import fromstring
from datetime import date
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
    trait = list(filter(lambda x: x['value'] == 'restaurant_menu', intents))[0]
    log.info(trait)
    return float(trait.get('confidence', 0)) > 0.6


def __send_wit_request(msg):
    global WIT_HEADERS
    rs = requests.get("https://api.wit.ai/message", {'q': msg}, headers=WIT_HEADERS)
    return rs.json()


def __get_todays_menu(xml_menu):
    today_string = date.today().strftime("%d/%m")
    recording = False
    ret = ""
    for chunk in xml_menu:
        text = chunk.text_content()
        if today_string in text:
            recording = True
            ret = "*{}*\n".format(text)
        elif recording:
            if 'Primeros:' in text or 'Segundos:' in text:
                ret = ret + "\n" + text + "\n"
            elif 'Postre:' in text:
                ret = ret + "\n" + text + "\n"
                return ret
            else:
                ret = ret + text + "\n"


def __get_menu():
    rq = Request("http://cafesbotiga.amadipesment.org/cafe-mirall/para-comer/", headers={'User-Agent': 'Some Browser'})
    with urlopen(rq) as f:
        data = f.read()
    doc = fromstring(data)
    msg = __get_todays_menu(doc.find_class("post-content")[0])
    return msg


@ec.on("message")
def response(event, client):
    qasimodo_cite = '<@{}>'.format(constants.qasimodo)
    if 'text' in event and (event['text'].startswith(qasimodo_cite) or event['text'].endswith(qasimodo_cite)):
        msg = event['text'].replace(qasimodo_cite, '')
        if __is_asking_for_menu(msg):
            menu = __get_menu()
            client.rtm_send_message(event['channel'], menu)



