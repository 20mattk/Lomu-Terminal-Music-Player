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


# Queue vs. Controller
# 1. History of Played Tracks:  Queue
# 2. Current Playing Track:     Controller
# 3. Queue of Upcoming Tracks:  Queue
# 4. Add, Remove, Clear Tracks: Queue
# 5. Shuffling:                 Queue
# 6. Going to Next Track:       Controller
# 7. Going to Previous Track:   Controller

# ============================================================================ #


from ..library import Track
from random import shuffle
# from threading import Lock


class PlaybackQueue:
    def __init__(self, tracks: list[Track] | None = None) -> None:
        self._tracks: list[Track] = (list(tracks) if tracks is not None else [])
        self._history: list[Track] = []

    # === immutable properties === #
    @property
    def tracks(self) -> tuple[Track, ...]:
        return tuple(self._tracks)

    @property
    def history(self) -> tuple[Track, ...]:
        return tuple(self._history)

    # === computed properties === #
    @property
    def queue_is_empty(self) -> bool:
        return not self._tracks

    @property
    def history_length(self) -> int:
        return len(self._history)

    @property
    def history_is_empty(self) -> bool:
        return not self._history

    # === utility methods === #
    def append_one(self, track: Track) -> None:
        self._tracks.append(track)

    def append_many(self, tracks: list[Track]) -> None:
        raise NotImplementedError

    def insert_at(self, track: Track, index: int) -> None:
        if 0 <= index <= len(self._tracks):
            self._tracks.insert(index, track)
        else:
            raise IndexError(f"Index {index} is out of bounds.")

    def remove_one(self, index: int) -> None:
        raise NotImplementedError

    def clear_all(self) -> None:
        raise NotImplementedError

    def pop_next(self) -> None:
        raise NotImplementedError

    def peek_next(self) -> None:
        raise NotImplementedError

    def shuffle(self) -> None:
        raise NotImplementedError

    # === dunder methods === #
    def __len__(self) -> int:
        return len(self._tracks)

    def __iter__(self):
        """Iterate over the upcoming Tracks."""
        return iter(self._tracks)

    def __contains__(self) -> None:
        """Check if a Track is in the queue."""
        raise NotImplementedError
