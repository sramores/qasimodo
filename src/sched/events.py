from sched import scheduler
from datetime import date

@scheduler.scheduled_job('cron', day_of_week='fri', hour=8)
def feria(**kwargs):
    msn = ""
    chn = "qa_group"

    today = date.today()
    feria = date(2018, 5, 18)

    days = feria - today

    if feria == today:
        msn = ("Mañana empieza la feria de Cordoba. :tada: :dancer: :confetti_ball: :dancers:")
    elif today < feria:
        msn = ("Sólo faltan " + str(days.days) + " días para la feria de Cordoba. :tada: :dancer:")

    client = kwargs['client']
    client.rtm_send_message(chn, msn)
