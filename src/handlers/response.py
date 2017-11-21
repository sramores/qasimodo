from . import event_controller as ec
from random import randint
import constants


@ec.on("message")
def response(event, client):
    	if 'text' in event and 'qasimodo' in event['text']:
            msg = "k dise?"
        if event['user'] == constants.vsolis:
            msgBisente = ['Bisente pls, callate.', 'Sabes lo que eres. ¿No?', 'k dise Bisente']
            msg =  msgBisente[randint(0, len(msgBisente)-1)]
        if event['user'] == constants.semartin:
            msg = "Eres increible"
        if event['user'] == constants.jrios:
            msg = "Loco, yo no soy de letras"
        if event['user'] ==constants.jariza:
           msgCordobe = ['k dise cordobe.', 'Toca bacat del dìa', 'Mas sospechoso que un gitano haciendo footing']
           msg =  msgCordobe[randint(0, len(msgCordobe)-1)]
        
        client.rtm_send_message(event['channel'], msg)
			

