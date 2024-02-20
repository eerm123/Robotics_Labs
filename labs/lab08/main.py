import signal
import sys

from PyQt5.QtWidgets import QApplication
from source.helper.current_state import CurrentState
from source.strategy.camera_strategy import CameraStrategy
from source.strategy.encoder_strategy import EncoderStrategy
from source.strategy.marker_strategy import MarkerStrategy
from source.strategy.ultrasonic_strategy import UltrasonicStrategy
from source.visuals.visualizer import Visualizer
from source.workers.robot_driver import Driver
from source.workers.strategy_worker import MeasuringWorker

app = QApplication([])


def main():
    signal.signal(signal.SIGTERM, shutdown_signal)
    signal.signal(signal.SIGINT, shutdown_signal)

    slow_worker = MeasuringWorker("slow", [CameraStrategy()])
    fast_worker = MeasuringWorker("fast", [UltrasonicStrategy(), EncoderStrategy(), MarkerStrategy()], 0.02)
    driver = Driver()
    visualizer = Visualizer(app, -1)

    try:
        slow_worker.start()
        fast_worker.start()
        driver.start()
        visualizer.start()
        print("Program finished execution")
    finally:
        close([slow_worker, fast_worker, driver])
        CurrentState().close()
        sys.exit()


def close(workers):
    print("Closing threads")
    for worker in workers:
        worker.should_close.set()
        worker.join()
    while any(worker.is_alive() for worker in workers):
        print("Waiting for threads to close")


def shutdown_signal(signal_number, frame):
    print("Program terminated manually with signal " + str(signal_number))
    app.quit()  # brake app loop, causes return from app.exec_()


if __name__ == "__main__":
    main()
