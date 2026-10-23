import pytest
from pathlib import Path

from lomu.playback import PlaybackQueue
from lomu.library import Track


@pytest.fixture
def tracks():
    return [
        Track(
            file_path=Path("track1.mp3"),
            title="Track One",
            artist="Artist A",
            album="Album A",
            release_date="2024",
            track_number=1,
            duration=180.0,
            album_art=b"\x89PNG\r\n\x1a\nAlbumArtImageA"
        ),
        Track(
            file_path=Path("track2.flac"),
            title="Track Two",
            artist="Artist B",
            album="Album B",
            release_date="2023",
            track_number=2,
            duration=210.0,
            album_art=b"\x89PNG\r\n\x1a\nAlbumArtImageB"
        ),
        Track(
            file_path=Path("track3.wav"),
            title="Track Three",
            artist="Artist C",
            album="Album C",
            release_date="2022",
            track_number=3,
            duration=240.0,
            album_art=b"\x89PNG\r\n\x1a\nAlbumArtImageC"
        ),
    ]


class TestPlaybackQueueInitialization:
    def test_initialization_empty_queue(self):
        """Test: Initialize empty queue is of PlaybackQueue type."""
        assert isinstance(PlaybackQueue(), PlaybackQueue)
    
    def test_initialize_queue_empty_list(self):
        """Test: Initialize queue with empty list is valid."""
        queue: PlaybackQueue = PlaybackQueue([])
        assert queue.tracks == ()
        assert len(queue) == 0

    def test_initialize_queue_empty_tuple(self):
        """Test: Initialize queue with empty tuple is valid."""
        queue: PlaybackQueue = PlaybackQueue(tuple())
        assert queue.tracks == ()
        assert len(queue) == 0

    def test_initialize_queue_tracks_list(self, tracks):
        """Test: Initialize queue with list of tracks is valid."""
        queue: PlaybackQueue = PlaybackQueue(tracks)
        assert queue.tracks == tuple(tracks)
        assert len(queue) == len(tracks)


"""
### 1. Initialization

- [x]Initialize an empty queue with no arguments.
- [x]Initialize an empty queue with an empty list.
- [x]Initialize an empty queue with an empty tuple.
- [x]Initialize a pre-populated queue with a list of tracks.
- [ ]Initialize a queue with a tuple of tracks.
- [ ]Initialize a queue with a generator of tracks.
- [ ]Verify the initial track order is preserved.
- [ ]Verify duplicate tracks are allowed during initialization.
- [ ]Raise `TypeError` if the initial iterable contains an invalid object.
- [ ]Verify initialization fails without creating a partially populated queue when a track is invalid.

### 2. `append_one()`

- [ ]Append a valid track to an empty queue.
- [ ]Append a valid track to a populated queue.
- [ ]Verify the track is added to the end.
- [ ]Verify the queue length increases by one.
- [ ]Append the same track multiple times.
- [ ]Raise `TypeError` when appending an invalid object.
- [ ]Verify the queue remains unchanged after an invalid append.

### 3. `append_many()`

- [ ]Append multiple tracks to an empty queue.
- [ ]Append multiple tracks to a populated queue.
- [ ]Append an empty list without changing the queue.
- [ ]Append an empty tuple without changing the queue.
- [ ]Append tracks from a generator.
- [ ]Verify the order of appended tracks is preserved.
- [ ]Verify the queue length increases by the number of appended tracks.
- [ ]Append multiple occurrences of the same track.
- [ ]Raise `TypeError` if any supplied object is not a `Track`.
- [ ]Verify no tracks are appended if validation fails, even when the invalid object appears after valid tracks in the iterable.

### 4. `insert_one_at()`

- [ ]Insert a track into an empty queue at index `0`.
- [ ]Insert a track at the beginning of a populated queue.
- [ ]Insert a track in the middle of a queue.
- [ ]Insert a track at the end using index `len(queue)`.
- [ ]Verify the existing tracks retain their relative order.
- [ ]Verify the queue length increases by one.
- [ ]Insert a duplicate track.
- [ ]Raise `TypeError` when the supplied track is invalid.
- [ ]Raise `TypeError` when the index is a float.
- [ ]Raise `TypeError` when the index is a string.
- [ ]Raise `TypeError` when the index is `True` or `False`.
- [ ]Raise `IndexError` for a negative index.
- [ ]Raise `IndexError` when the index exceeds `len(queue)`.
- [ ]Verify the queue remains unchanged after an invalid insertion.

### 5. `remove_one_at()`

- [ ]Remove the first track.
- [ ]Remove a track from the middle.
- [ ]Remove the last track.
- [ ]Remove the only track from a one-track queue.
- [ ]Verify the removed track is returned.
- [ ]Verify the remaining tracks preserve their relative order.
- [ ]Verify the queue length decreases by one.
- [ ]Raise `TypeError` when the index is a float.
- [ ]Raise `TypeError` when the index is a string.
- [ ]Raise `TypeError` when the index is `True` or `False`.
- [ ]Raise `IndexError` for a negative index.
- [ ]Raise `IndexError` when the index equals `len(queue)`.
- [ ]Raise `IndexError` when the index exceeds `len(queue)`.
- [ ]Raise `IndexError` when removing from an empty queue.
- [ ]Verify the queue remains unchanged after an invalid removal.

### 6. `clear_all()`

- [ ]Clear a populated queue.
- [ ]Verify the queue length becomes zero.
- [ ]Verify the queue contains no tracks afterward.
- [ ]Clear an already empty queue without raising an exception.
- [ ]Clear a queue multiple times without raising an exception.
- [ ]Verify previously returned `tracks` snapshots remain unchanged after clearing.

### 7. `pop_next()`

- [ ]Pop the first track from a populated queue.
- [ ]Verify the returned track is the first track originally in the queue.
- [ ]Verify exactly one track is removed.
- [ ]Verify the remaining tracks retain their relative order.
- [ ]Pop the only track from a one-track queue.
- [ ]Verify the queue becomes empty after popping its only track.
- [ ]Raise `IndexError` when popping from an empty queue.

### 8. `peek_next()`

- [ ]Peek at the first track in a populated queue.
- [ ]Verify the returned track is the first track.
- [ ]Verify the queue contents remain unchanged.
- [ ]Verify the queue length remains unchanged.
- [ ]Peek at a one-track queue.
- [ ]Raise `IndexError` when peeking at an empty queue.
- [ ]Verify repeated peeks return the same first track if no mutations occur.

### 9. `move_track()`

- [ ]Move the first track to the end.
- [ ]Move the last track to the beginning.
- [ ]Move a track forward by one position.
- [ ]Move a track backward by one position.
- [ ]Move a track several positions forward.
- [ ]Move a track several positions backward.
- [ ]Move a track to its current index and verify the queue is unchanged.
- [ ]Verify the queue length remains unchanged after a successful move.
- [ ]Verify all other tracks preserve their relative order.
- [ ]Raise `TypeError` when the source index is a float.
- [ ]Raise `TypeError` when the destination index is a float.
- [ ]Raise `TypeError` when either index is a string.
- [ ]Raise `TypeError` when either index is `True` or `False`.
- [ ]Raise `IndexError` when the source index is negative.
- [ ]Raise `IndexError` when the destination index is negative.
- [ ]Raise `IndexError` when the source index equals `len(queue)`.
- [ ]Raise `IndexError` when the destination index equals `len(queue)`.
- [ ]Raise `IndexError` when either index exceeds `len(queue)`.
- [ ]Raise `IndexError` when moving a track in an empty queue.
- [ ]Verify the queue remains unchanged after an invalid source index.
- [ ]Verify the queue remains unchanged after an invalid destination index.

### 10. `shuffle()`

- [ ]Shuffle a populated queue without raising an exception.
- [ ]Verify the queue length remains unchanged.
- [ ]Verify all original entries remain present after shuffling.
- [ ]Verify duplicate tracks retain their original occurrence counts.
- [ ]Shuffle an empty queue without raising an exception.
- [ ]Shuffle a one-track queue without changing its contents.
- [ ]Shuffle a queue containing duplicate tracks.
- [ ]Shuffle the queue multiple times without losing or adding entries.

Do not assert that a shuffle must produce a different order. Randomly obtaining the original order is valid behavior.

### 11. `tracks` property

- [ ]Verify `tracks` returns a tuple.
- [ ]Verify the tuple contains all queue entries in order.
- [ ]Verify the tuple is empty for an empty queue.
- [ ]Verify the returned tuple cannot be modified.
- [ ]Verify appending to a list created from the tuple does not affect the queue.
- [ ]Verify clearing a list created from the tuple does not affect the queue.
- [ ]Verify a previously returned snapshot does not change after appending a track.
- [ ]Verify a previously returned snapshot does not change after removing a track.
- [ ]Verify a previously returned snapshot does not change after clearing the queue.
- [ ]Verify a previously returned snapshot does not change after shuffling the queue.

### 12. `__len__()`

- [ ]Return zero for an empty queue.
- [ ]Return the correct count for a populated queue.
- [ ]Return the correct count after appending a track.
- [ ]Return the correct count after appending multiple tracks.
- [ ]Return the correct count after inserting a track.
- [ ]Return the correct count after removing a track.
- [ ]Return the correct count after popping a track.
- [ ]Return zero after clearing the queue.
- [ ]Return the same count before and after shuffling or moving tracks.

### 13. `__iter__()`

- [ ]Iterate over an empty queue without yielding any tracks.
- [ ]Iterate over a populated queue in the correct order.
- [ ]Verify the iterator yields every track exactly once per occurrence.
- [ ]Verify duplicate tracks are yielded the correct number of times.
- [ ]Verify `list(queue)` matches `list(queue.tracks)`.
- [ ]Verify iterating over the queue does not modify it.

### 14. `__contains__()`

- [ ]Return `True` when a track is present.
- [ ]Return `False` when a track is absent.
- [ ]Return `False` when checking an empty queue.
- [ ]Return `True` when a track appears multiple times.
- [ ]Return `False` after the only occurrence of a track is removed.
- [ ]Return `True` after appending a previously absent track.
- [ ]Return `False` after clearing the queue.
- [ ]Verify membership checks do not modify the queue.
- [ ]Verify a non-`Track` object returns `False` when it is not present.

### 15. Cross-method consistency and invariants

- [ ]Verify `len(queue) == len(queue.tracks)` after every mutation.
- [ ]Verify `list(queue) == list(queue.tracks)` after every mutation.
- [ ]Verify every queued entry is a `Track`.
- [ ]Verify adding and then removing a track restores the original contents.
- [ ]Verify popping all tracks returns them in their original order.
- [ ]Verify clearing and then repopulating the queue works correctly.
- [ ]Verify a sequence of mixed operations maintains the correct contents and order.
- [ ]Verify failed operations do not mutate the queue.
- [ ]Verify repeated operations on an empty queue behave according to the documented exceptions.
"""