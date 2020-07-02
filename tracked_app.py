import atexit
import sys
from contextlib import redirect_stdout, redirect_stderr


class Tee(object):
    def __init__(self, dest1, dest2):
        self.dest1 = dest1
        self.dest2 = dest2

    def __del__(self):
        pass

    def flush(self):
        self.dest1.flush()
        self.dest2.flush()

    def write(self, message):
        self.dest1.write(message)
        self.dest2.write(message)


class Publisher(object):
    def __init__(self):
        self.f = []

    def __del__(self):
        pass

    def subscribe(self, callback):
        self.f.append(callback)

    def unsubscribe(self, callback):
        self.f.remove(callback)

    def flush(self):
        for x in self.f:
            x.flush()

    def write(self, message):
        for x in self.f:
            x.write(message)


class TrackedApp:
    def __init__(self, f):
        self.f = f
        self.c_stdout = Publisher()
        self.c_stderr = Publisher()

    def run(self):
        with redirect_stdout(Tee(self.c_stdout, sys.stdout)):
            with redirect_stderr(Tee(self.c_stderr, sys.stderr)):
                self.f(self)

    def register_stdout(self, callback):
        self.c_stdout.subscribe(callback)

    def register_sterr(self, callback):
        self.c_stderr.subscribe(callback)