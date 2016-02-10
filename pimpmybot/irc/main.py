from .client import Client


def run(pipe):
    client = Client()
    client.connect()
    client.run()