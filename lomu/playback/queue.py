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
    
    # === immutable properties === #
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
    
    # @property
    # def repeat_mode(self) -> RepeatMode:
    #     """Return the currently-set repeat mode of the queue."""
    #     return self._repeat_mode

    # @property
    # def shuffle_enabled(self) -> bool:
    #     """Return the currently-set shuffle toggle of the queue."""
    #     return self._shuffle_enabled
    
    # === utility methods === #
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

        if (
            self._current_index is not None 
            and not (0 <= self._current_index < len(self._queue))
        ):
            raise RuntimeError("The current index is out of bounds.")

        if self._current_index is None:
            self._current_index = 0
        elif self._current_index < len(self._queue) - 1:
            self._current_index += 1
        elif self._current_index == len(self._queue) - 1:
            if self._repeat_mode == RepeatMode.ALL:
                self._current_index = 0
            # otherwise, stay at the end
        else:
            raise RuntimeError("The current index is invalid.")

        return self._queue[self._current_index]

        # release lock

    def previous(self) -> Track | None:
        """Return to the previous Track object in the playback queue."""
        # acquire lock

        if not self._queue:
            return None

        if (
            self._current_index is not None 
            and not (0 <= self._current_index < len(self._queue))
        ):
            raise RuntimeError("The current index is out of bounds.")

        if self._current_index is None:
            self._current_index = 0
        elif self._current_index > 0:
            self._current_index -= 1
        elif self._current_index == 0:
            if self._repeat_mode == RepeatMode.ALL:
                self._current_index = len(self._queue) - 1
            # otherwise, stay at the start
        else:
            raise RuntimeError("The current index is invalid.")

        return self._queue[self._current_index]

        # release lock
    
    # def set_repeat_mode(self, mode: RepeatMode) -> None:
    #     """Set the repeat mode of the queue."""
    #     # acquire lock
    #     if not isinstance(mode, RepeatMode):
    #         raise TypeError("Repeat mode must be of RepeatMode.")

    #     self._repeat_mode = mode
    #     # release lock

    # add some stuff for shuffling