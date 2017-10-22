from . import event_controller as ec


@ec.on("member_joined_channel")
def greet(event, client):
    message = "Welcome <@{}>".format(event['user'])
    client.rtm_send_message(event['channel'], message)

