from multiprocessing import freeze_support

from wsgi import app


if __name__ == "__main__":
    freeze_support()
    app.run()
