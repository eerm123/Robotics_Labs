import threading
from threading import Thread

from ..solutions.drive_logic import follow_line
from ..helper.current_state import CurrentState

class Driver(Thread):
    def __init__(self):
        super().__init__(name="driver")
        self.should_close = threading.Event()
        self.current_state = CurrentState()

    def run(self):
        follow_line(self.should_close)
        print("closing " + self.name)
