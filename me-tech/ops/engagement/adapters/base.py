import time
import random

class BaseAdapter:
    def __init__(self, port: int):
        self.port = port

    def random_delay(self, min_s: float = 3.0, max_s: float = 7.0) -> None:
        delay = random.uniform(min_s, max_s)
        time.sleep(delay)
