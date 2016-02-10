from multiprocessing import Process, Pipe

from wsgi.main import run as wsgi_run
from irc.main import run as irc_run


if __name__ == "__main__":
    # We fork the process, the parent is the wsgi so it can get the bot status and restart it if needed.
    wsgi_pipe, irc_pipe = Pipe()
    irc_process = Process(target=irc_run, args=(irc_pipe,))
    irc_process.start()
    wsgi_run(wsgi_pipe, irc_process)
