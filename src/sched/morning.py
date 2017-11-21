from sched import scheduler
from random import randint
import datetime


days_of_week = ['lunes', 'martes', 'miércoles', 'jueves',
                'viernes', 'sábado', 'domingo']
greetings = ['¡Buenos días!', '¡Que tengáis un fantástico día!',
             'Good morning', 'Que paseis un buen {}', 'Buen {}', 'Buenos días por la mañana']

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=8)
def morning(**kwargs):
    msg = greetings[randint(0, len(greetings)-1)]
    day = days_of_week[datetime.datetime.today().weekday()]
    msg = msg.format(day)

    client = kwargs['client']
    client.rtm_send_message("qa_group", msg)
