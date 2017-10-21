import sys


class Qasimodo(object):
    
    def __init__(self, token):
        pass








if __name__ == '__main__':
    if len(sys.argv) > 1:
        token = sys.argv[1]
    elif 'BOT_TOKEN' in os.environ:
        token = os.environ['BOT_TOKEN']
    else:
        raise Exception('No token found for the bot')

    qasimodo = Qasimodo(token)

