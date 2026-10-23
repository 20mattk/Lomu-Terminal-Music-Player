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
        """
        Append one Track to the end of the queue.

        Arguments:
            track (Track): The track to append to the queue.
        
        Raises:
            (TypeError): If the track supplied is not a Track instance.
        """
        self._validate_track(track)
        self._tracks.append(track)

    def append_many(self, tracks: Iterable[Track]) -> None:
        """
        Append many Track instances to the end of the queue.

        Arguments:
            tracks (Iterable[Track]): The Track instances to add.
        
        Raises:
            (TypeError): If the track supplied is not a Track instance.
        """
        new_tracks: list[Track] = list(tracks)

        for track in new_tracks:
            self._validate_track(track)

        self._tracks.extend(new_tracks)

    def insert_one_at(self, index: int, track: Track) -> None:
        """
        Insert one Track instance at a certain location in the queue.

        Arguments:
            index (int): The index location to insert at.
            track (Track): The Track instance to insert.
        
        Raises:
            (TypeError): If the track supplied is not a Track instance.
            (TypeError): If the index supplied is not an integer.
            (IndexError): If the index supplied is out of bounds.
        """
        self._validate_track(track)
        self._validate_index(index, include_end=True)
        self._tracks.insert(index, track)

    def remove_one_at(self, index: int) -> Track:
        """
        Remove one Track instance at a certain location in the queue.

        Arguments:
            index (int): The index location to remove at.
        
        Returns:
            (Track): The Track instance which was removed from the queue.
        
        Raises:
            (TypeError): If the index supplied is not an integer.
            (IndexError): If the index supplied is out of bounds.
        """
        self._validate_index(index)
        return self._tracks.pop(index)

    def clear_all(self) -> None:
        """Clear all Tracks from the queue."""
        self._tracks.clear()

    def pop_next(self) -> Track:
        """
        Pop the next-up Track from the top of the queue.

        Returns:
            (Track): The Track popped from the queue.
        
        Raises:
            (IndexError): If the queue is empty.
        """
        if not self._tracks:
            raise IndexError("The queue is empty.")

        return self._tracks.pop(0)

    def peek_next(self) -> Track:
        """
        Peek the next-up Track that is at the top of the queue.

        Returns:
            (Track): The Track next up in the queue.
        
        Raises:
            (IndexError): If the queue is empty.
        """
        if not self._tracks:
            raise IndexError("The queue is empty.")

        return self._tracks[0]

    def move_track(self, old_index: int, new_index: int) -> None:
        """
        Move a Track from one spot to another in the queue.

        Arguments:
            old_index (int): The index of the Track to move.
            new_index (int): The index to move the Track to.
        
        Raises:
            (TypeError): If either index supplied is not an integer.
            (IndexError): If the either index supplied is out of bounds.
        """
        self._validate_index(old_index)
        self._validate_index(new_index)

        if old_index == new_index:
            return

        track: Track = self._tracks.pop(old_index)
        self._tracks.insert(new_index, track)

    def shuffle(self) -> None:
        """Shuffle the order of the queue."""
        # future: shuffle tracks in current "context" (album, playlist, etc.)
        random_shuffle(self._tracks)

    # === helper methods === #
    def _validate_track(self, track: object) -> None:
        """
        Validate that the object is a Track instance.

        Arguments:
            track (object): The object to validate.
        
        Raises:
            (TypeError): The supplied object is not an instance of Track.
        """
        if not isinstance(track, Track):
            raise TypeError(f"Not a valid Track instance: {track}.")

    def _validate_index(self, index: int, include_end: bool = False) -> None:
        """
        Validate that an index is an integer and in bounds of the queue.

        Arguments:
            index (int): The index to validate.
            include_end (bool): If True, upper bound is length of the queue. If
                                False, upper bound is length of the queue - 1.
        
        Raises:
            (TypeError): If the index is not an integer.
            (IndexError): If the index is not within valid bounds.
        """
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError(f"Index must be an integer, not {type(index)}.")

        upper_bound: int = (
            len(self._tracks) if include_end else len(self._tracks) - 1
        )

        if not 0 <= index <= upper_bound:
            raise IndexError(f"Index {index} is out of bounds.")

    # === dunder methods === #
    def __len__(self) -> int:
        """Return the number of Tracks in the queue."""
        return len(self._tracks)

    def __iter__(self) -> Iterator[Track]:
        """Iterate over the upcoming Tracks."""
        return iter(self._tracks)

    def __contains__(self, track: object) -> bool:
        """Check if a Track is in the queue."""
        return track in self._tracks
