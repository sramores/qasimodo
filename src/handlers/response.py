from . import event_controller as ec
import constants


@ec.on("message")
def response(event, client):
    if 'text' in event and 'qasimodo' in event['text']:
        msg = "k dise?"
        if event['user'] == constants.vsolis:
            msg = "k dise bisente?"

        client.rtm_send_message(event['channel'], msg)

