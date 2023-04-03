import threading

class background_worker:
    def __init__(self, workers: list):
        self._threads = None
        self._workers = workers
        self._stop_events = [threading.Event() for _ in self._workers]

    def start(self):
        self._threads = [threading.Thread(target=self._workers[i], args=(self._stop_events[i],)) for i in range(len(self._workers))]
        for thread in self._threads:
            thread.start()

    def stop(self):
        for index, thread in enumerate(self._threads):
            self._stop_events[index].set()
            thread.join()
        self._threads.clear()
        self._threads = None
