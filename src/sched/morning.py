from sched import scheduler


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=8)
def morning(**kwargs):
    client = kwargs['client']
    client.rtm_send_message("qasimodo_pruebas", 'Buenos dias!')
