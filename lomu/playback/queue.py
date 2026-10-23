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

# !!! HISTORY MIGHT BECOME ITS OWN MODULE AT SOME POINT !!!

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
from random import shuffle as random_shuffle
from collections.abc import Iterator, Iterable
# from threading import Lock


class PlaybackQueue:
    def __init__(self, tracks: Iterable[Track] | None = None) -> None:
        self._tracks: list[Track] = []

        if tracks is not None:
            self.append_many(tracks)

    # === immutable properties === #
    @property
    def tracks(self) -> tuple[Track, ...]:
        """Return the queue as an immutable Tuple of Tracks."""
        return tuple(self._tracks)

    # === utility methods === #
    def append_one(self, track: Track) -> None:
        self._validate_track(track)
        self._tracks.append(track)

    def append_many(self, tracks: Iterable[Track]) -> None:
        new_tracks: list[Track] = list(tracks)

        for track in new_tracks:
            self._validate_track(track)

        self._tracks.extend(new_tracks)

    def insert_one_at(self, index: int, track: Track) -> None:
        self._validate_track(track)
        self._validate_index(index, include_end=True)
        self._tracks.insert(index, track)

    def remove_one_at(self, index: int) -> Track:
        self._validate_index(index)
        return self._tracks.pop(index)

    def clear_all(self) -> None:
        self._tracks.clear()

    def pop_next(self) -> Track:
        if not self._tracks:
            raise IndexError("The queue is empty.")

        return self._tracks.pop(0)

    def peek_next(self) -> Track:
        if not self._tracks:
            raise IndexError("The queue is empty.")

        return self._tracks[0]

    def move_track(self, old_index: int, new_index: int) -> None:
        self._validate_index(old_index)
        self._validate_index(new_index)

        if old_index == new_index:
            return

        track: Track = self._tracks.pop(old_index)
        self._tracks.insert(new_index, track)

    def shuffle(self) -> None:
        # future: shuffle tracks in current "context" (album, playlist, etc.)
        random_shuffle(self._tracks)

    # === helper methods === #
    def _validate_track(self, track: Track) -> None:
        if not isinstance(track, Track):
            raise TypeError(f"Not a valid Track instance: {track}.")

    def _validate_index(self, index: int, include_end: bool = False) -> None:
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError(f"Index must be an integer, not {type(index)}.")

        upper_bound: int = (
            len(self._tracks) if include_end else len(self._tracks) - 1
        )

        if not 0 <= index <= upper_bound:
            raise IndexError(f"Index {index} is out of bounds.")

    # === dunder methods === #
    def __len__(self) -> int:
        return len(self._tracks)

    def __iter__(self) -> Iterator[Track]:
        """Iterate over the upcoming Tracks."""
        return iter(self._tracks)

    def __contains__(self, track: object) -> bool:
        """Check if a Track is in the queue."""
        return track in self._tracks
