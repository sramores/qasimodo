from . import event_controller as ec


@ec.on("message")
def response(event, client):
    if 'qasimodo' in event['text']:
        client.rtm_send_message(event['channel'], "k dise?")

