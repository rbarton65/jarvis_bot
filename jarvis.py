import socket
import sys
import json
import argparse


from src.respond import interpret

parser = argparse.ArgumentParser(description='Start bot server.')
parser.add_argument('--port', '-p',  type=int, required=True,
                    help='port number for bot to listen for data')
parser.add_argument('--id', '-i', required=True,
                            help='bot id from groupme')

args = parser.parse_args()


class Message(object):
    '''Organizes message'''
    def __init__(self, **message_info):
        self.__dict__.update(message_info)

#    def _check_keys(self):
#        keys = ['id', 'user_id', 'attachments', 'name', 'text',
#                'group_id', 'sender_type', 'system', 'avatar_url',
#                'sender_id', 'created_at', 'source_guid']


def _fetch_message_info(data):
    '''Decodes message'''
    data = json.loads(data.decode('utf-8').split('\n')[-1])
    message = Message(**data)
    return message


def listen(port, bot_id, host=''):
    '''Creates a port listening socket server'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

    except socket.error as msg:
        print('Bind failed. Error Code: %s Message %s' % (msg[0], msg[1]))
        sys.exit()

    s.listen(10)

    while 1:
        # wait for a connection
        conn, addr = s.accept()

        try:
            data = conn.recv(1024)
            message = _fetch_message_info(data)
            if message.sender_type == "user":
                interpret(message, bot_id)

        except:
            pass
    s.close()


def main():
    listen(args.port, args.id)

if __name__ == '__main__':
    main()
