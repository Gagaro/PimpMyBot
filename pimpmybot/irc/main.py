import socket

HOST = 'irc.twitch.tv'
PORT = 6667
USERNAME = None
OAUTH = None


def run(pipe):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send('PASS oauth:{0}\r\n'.format(OAUTH).encode('utf8'))
    s.send('NICK {0}\r\n'.format(USERNAME).encode('utf8'))
    while True:
        print(s.recv(1024).decode())
        print('\n')
    s.close()