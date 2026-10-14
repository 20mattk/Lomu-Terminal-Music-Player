from enum import Enum, auto
from ..library import Track
# from threading import Lock


class RepeatMode(Enum):
    OFF = auto()
    ALL = auto()
    ONE = auto()


class PlaybackQueue:
    def __init__(self, tracks: list[Track]):
        self._queue: list[Track] = list(tracks)
        self._current_index: int | None = 0 if self._queue else None
        self._repeat_mode: RepeatMode = RepeatMode.OFF
        self._shuffle_enabled: bool = False
        # self._lock = None
    
    # immutable properties
    @property
    def queue(self) -> list[Track] | list[None]:
        """Return a copy of the internal Track object list."""
        # acquire lock
        return list(self._queue)
        # release lock
    
    @property
    def current_track(self) -> Track | None:
        """Return the Track object at the current index."""
        # acquire lock
        if self._current_index is None:
            return None

        return self._queue[self._current_index]
        # release lock
    
    # utility methods
    def add(self, track: Track) -> None:
        """Add a Track object to the playback queue."""
        # acquire lock
        self._queue.append(track)
        # release lock

    def clear(self) -> None:
        """Clear all Track objects from the playback queue."""
        # acquire lock
        self._queue.clear()
        self._current_index = None
        # release lock

    def next(self) -> Track | None:
        """Skip to the next Track object in the playback queue."""
        # acquire lock

        if not self._queue:
            return None

        if self._repeat_mode == RepeatMode.ONE:
            return self.current_track

        if self._current_index is None:
            self._current_index = 0
        elif self._current_index < len(self._queue) - 1:
            self._current_index += 1
        elif (self._current_index == len(self._queue) - 1
              and self._repeat_mode == RepeatMode.ALL):
            self._current_index = 0
        else:
            self._current_index = None
            return None

        return self._queue[self._current_index]

        # release lock

    def previous(self) -> Track | None:
        """Return to the previous Track object in the playback queue."""
        # acquire lock

        if not self._queue:
            return None

        if self._repeat_mode == RepeatMode.ONE:
            return self.current_track

        if self._current_index is None:
            return None
        elif self._current_index > 0:
            self._current_index -= 1
        elif self._repeat_mode == RepeatMode.ALL:
            self._current_index = len(self._queue) - 1
        else:
            self._current_index = None
            return None

        return self._queue[self._current_index]

        # release lock
    
    # add some stuff for shuffling