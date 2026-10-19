# === TODO =================================================================== #

# I will re-structure the playback module according to the below:
# lomu/
# └── playback/
#     ├── __init__.py
#     ├── context.py     # Track scope/eligibility for current playback session
#     ├── queue.py       # Ordering and shuffling of Tracks in the Queue
#     ├── controller.py  # Track playback state (play/next, etc, send to Player)
#     ├── player.py      # Audio playback with VLC and event reporting
#     └── events.py      # Defines events to be reported by the Player

# Development Order:
# 1. context.py
# 2. queue.py
# 3. events.py
# 4. player.py
# 5. controller.py

# ============================================================================ #


from ..library import Track
from random import shuffle
# from threading import Lock


class PlaybackQueue:
    def __init__(self, tracks: list[Track]) -> None:
        self._queue: list[Track] = list(tracks)
        self._position: int = 0

    # === immutable properties === #
    @property
    def queue(self) -> list[Track]:
        return self._queue

    @property
    def position(self) -> int:
        return self._position

    # === computed properties === #
    @property
    def length(self) -> int:
        return len(self._queue)

    @property
    def is_empty(self) -> bool:
        return not self._queue

    # === utility methods === #
    def get_track(self) -> Track:
        if self.is_empty:
            raise ValueError("The queue is empty.")

        return self._queue[self._position]

    def add(self, track: Track, index: int | None = None) -> None:
        if not isinstance(track, Track):
            raise ValueError("You may only add Track objects to the queue.")

        if not index:
            self._queue.append(track)
        elif 0 <= index < len(self._queue):
            self.queue.insert(index, track)
        else:
            raise IndexError("Insertion index is out of bounds.")

    def remove(self, index: int) -> None:
        if index == self._position:
            raise ValueError("Cannot remove the current Track from the queue.")

        if not index or index < 0 or index >= len(self._queue):
            raise IndexError("Removal index is invalid.")

        self._queue.pop(index)

    def clear(self) -> None:
        self._queue.clear()
        self._position = 0

    def shuffle(self) -> None:
        shuffle(self._queue)
        self._position = 0
