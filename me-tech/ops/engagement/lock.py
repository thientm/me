import os
import time

def check_conflicts(lock_paths: list[str]) -> bool:
    for path in lock_paths:
        if os.path.exists(path):
            return True
    return False

class EngagementLock:
    def __init__(self, lock_path: str):
        self.lock_path = lock_path
        self._acquired = False

    def acquire(self) -> bool:
        if os.path.exists(self.lock_path):
            return False
        try:
            os.makedirs(os.path.dirname(os.path.abspath(self.lock_path)), exist_ok=True)
            with open(self.lock_path, "x") as f:
                f.write(f"{os.getpid()}:{time.time()}\n")
            self._acquired = True
            return True
        except FileExistsError:
            return False

    def release(self) -> None:
        if self._acquired and os.path.exists(self.lock_path):
            try:
                os.remove(self.lock_path)
            except OSError:
                pass
            self._acquired = False

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
