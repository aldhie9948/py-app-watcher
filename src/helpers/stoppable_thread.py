import threading
import time


class StoppableThread:
    def __init__(self):
        self.thread = None
        self.stop_flag = threading.Event()

    def start(self, target_func, *args, **kwargs):
        if self.thread and self.thread.is_alive():
            return False

        self.stop_flag.clear()
        self.thread = threading.Thread(
            target=self._wrapper, args=(target_func, args, kwargs), daemon=True
        )
        self.thread.start()
        return True

    def _wrapper(self, func, args, kwargs):
        try:
            func(self.stop_flag, *args, **kwargs)
        except Exception as e:
            print(f"Error di thread: {e}")

    def stop(self):
        self.stop_flag.set()
        if self.thread:
            self.thread.join(timeout=2)

    def is_running(self):
        return self.thread and self.thread.is_alive()
