import socket

from common.config import Configuration

HOST = 'irc.twitch.tv'
PORT = 6667


def run(pipe):
    config = Configuration.get_or_create()[0]
    if not config.username or not config.oauth:
        print("NOT CONFIGURED YET, LEAVING")
        return

    s = socket.socket()
    s.connect((HOST, PORT))
    s.send('PASS {0}\r\n'.format(config.oauth).encode('utf8'))
    s.send('NICK {0}\r\n'.format(config.username).encode('utf8'))
    while True:
        response = s.recv(1024).decode().strip()
        if response:
            print(response)
            print('\n')
    s.close()
