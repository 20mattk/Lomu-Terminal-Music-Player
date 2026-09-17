from ..library import Library, Track
from queue import Queue, Full, Empty
import random


class Queue:
    MAX_SIZE: int = 5_000

    def __init__(self, library: Library):
        self._library: Library = library
        self._queue: Queue = Queue(maxsize=self.MAX_SIZE)

    def add(self, track: Track) -> None:
        """Add a single Track to the queue for processing."""
        if not isinstance(track, Track):
            raise TypeError("Cannot add an object not of type Track.")
        if self._queue.is_full():
            raise Full(f"Queue is at maximum Track capacity. ({MAX_SIZE})")
        self._queue.put(track, block=True)

    def next(self, timeout: int = 5) -> Track:
        """Retrieves the next Track in the queue. Blocks if empty."""
        try:
            return self._queue.get(block=True, timeout=timeout)
        except Empty:
            raise TimeoutError("The queue is empty.")
        except:
            raise Exception("Something went wrong.")
        
    def is_empty(self) -> bool:
        """Returns True/False if the queue is empty or not."""
        return self._queue.empty()
    
    def is_full(self) -> bool:
        """Returns True/False if the queue is full or not."""
        return self._queue.full()
    
    def length(self) -> int:
        """Returns the length of the queue in number of Track objects."""
        return self._queue.qsize()