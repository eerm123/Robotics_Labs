# -*- coding: utf-8 -*-

import threading
from threading import Thread

from ..solutions.drive_logic import follow_line


class Driver(Thread):
    def __init__(self):
        super().__init__(name="driver")
        self.should_close = threading.Event()

    def run(self):
        follow_line(self.should_close)
        print("closing " + self.name)
