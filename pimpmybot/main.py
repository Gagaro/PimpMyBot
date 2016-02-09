from multiprocessing import Process, Pipe

from wsgi.main import run as wsgi_run
from irc.main import run as irc_run


if __name__ == "__main__":
    # We fork into two processes, the web server and the irc bot
    wsgi_pipe, irc_pipe = Pipe()
    wsgi_process = Process(target=wsgi_run, args=(wsgi_pipe,))
    irc_process = Process(target=irc_run, args=(irc_pipe,))
    irc_process.start()
    wsgi_process.start()
    irc_process.join()
    wsgi_process.join()