import pytest
from pathlib import Path

from lomu.playback import PlaybackQueue
from lomu.library import Track


@pytest.fixture
def empty_queue():
    return PlaybackQueue()

@pytest.fixture
def populated_queue():
    return PlaybackQueue([
        Track(
            file_path=Path("existing_track.mp3"),
            title="Exiting Track",
            artist="Exiting Artist",
            album="Exiting Album",
            release_date="2006",
            track_number=11,
            duration=149.0,
            album_art=b"\x89PNG\r\n\x1a\nExistingAlbumArt"
        ),
        Track(
            file_path=Path("ahhhh.mp3"),
            title="AHHH",
            artist="Person",
            album="Albummmmm",
            release_date="1987",
            track_number=8,
            duration=10.0,
            album_art=b"\x89PNG\r\n\x1a\nUGH"
        )
    ])

@pytest.fixture
def track():
    return Track(
        file_path=Path("test_track.mp3"),
        title="Test Track",
        artist="Test Artist",
        album="Test Album",
        release_date="2001",
        track_number=1,
        duration=180.0,
        album_art=b"\x89PNG\r\n\x1a\nTestAlbumArt"
    )

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
        """Test: Initialize queue with empty list."""
        queue: PlaybackQueue = PlaybackQueue([])
        assert queue.tracks == ()
        assert len(queue) == 0

    def test_initialize_queue_empty_tuple(self):
        """Test: Initialize queue with empty tuple."""
        queue: PlaybackQueue = PlaybackQueue(tuple())
        assert queue.tracks == ()
        assert len(queue) == 0

    def test_initialize_queue_tracks_list(self, tracks):
        """Test: Initialize queue with list of tracks."""
        queue: PlaybackQueue = PlaybackQueue(tracks)
        assert queue.tracks == tuple(tracks)
        assert len(queue) == len(tracks)

    def test_initialize_queue_track_tuple(self, tracks):
        """Test: Initialize queue with tuple of tracks."""
        queue: PlaybackQueue = PlaybackQueue(tuple(tracks))
        assert queue.tracks == tuple(tracks)
        assert len(queue) == len(tracks)

    def test_initialize_queue_duplicate_tracks_allowed(self, tracks):
        """Test: Initialize queue with duplicate tracks is safe."""
        tracks.append(tracks[0])
        queue: PlaybackQueue = PlaybackQueue(tracks)
        assert queue.tracks == tuple(tracks)
        assert len(queue) == len(tracks)

    def test_initialize_queue_fails_invalid_track(self, tracks):
        """Test: Initialize queue with an invalid track raises a TypeError."""
        tracks.append("INVALID")
        with pytest.raises(TypeError):
            queue: PlaybackQueue = PlaybackQueue(tracks)


class TestPlaybackQueueAppendOne:
    def test_append_one_valid_track_empty_queue(self, empty_queue, track):
        """Test: Appending a valid track to an empty queue works."""
        empty_queue.append_one(track)
        print(empty_queue.tracks)
        assert empty_queue.tracks == tuple([track])
        assert len(empty_queue) == len(tuple([track]))

    def test_append_one_track_populated_queue(self, populated_queue, track):
        """Test: Appending a track to a populated queue."""
        original_length: int = len(populated_queue)
        populated_queue.append_one(track)
        assert len(populated_queue) == original_length + 1

    def test_append_one_adds_to_end(self, populated_queue, track):
        """Test: Appending a track to a populated queue is at the end."""
        populated_queue.append_one(track)
        assert populated_queue.tracks[-1] == track

    def test_append_one_same_track_multiple_times(self, empty_queue, track):
        """Test: Able to append one track multiple times."""
        empty_queue.append_one(track)
        assert len(empty_queue) == 1
        empty_queue.append_one(track)
        assert len(empty_queue) == 2

    def test_append_one_invalid_track_errors(self, empty_queue):
        """Test: TypeError raised when invalid object appended."""
        with pytest.raises(TypeError):
            empty_queue.append_one("NOT_A_TRACK")

    def test_append_one_invalid_keeps_queue_state(self, populated_queue):
        """Test: Appending invalid object leaves queue unchanged."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(TypeError):
            populated_queue.append_one("NOT_A_TRACK")
        assert populated_queue.tracks == before_tracks
        assert len(populated_queue) == len(before_tracks)


class TestPlaybackQueueAppendMany:
    def test_append_many_tracks_empty_queue(self, empty_queue, tracks):
        """Test: Append many tracks to an empty queue."""
        empty_queue.append_many(tracks)
        assert empty_queue.tracks == tuple(tracks)
        assert len(empty_queue) == len(tracks)

    def test_append_many_tracks_populated_queue(self, populated_queue, tracks):
        """Test: Append many tracks to an empty queue."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.append_many(tracks)
        assert populated_queue.tracks == before_tracks + tuple(tracks)
        assert len(populated_queue) == len(before_tracks) + len(tracks)

    def test_append_many_empty_list_to_queue(self, populated_queue):
        """Test: Appending empty list to populated queue doesn't change it."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.append_many([])
        assert populated_queue.tracks == before_tracks
        assert len(populated_queue) == len(before_tracks)

    def test_append_many_empty_tuple_to_queue(self, populated_queue):
        """Test: Appending empty tuple to populated queue doesn't change it."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.append_many(tuple())
        assert populated_queue.tracks == before_tracks
        assert len(populated_queue) == len(before_tracks)

    def test_append_many_preserves_order(self, populated_queue, tracks):
        """Test: Appending many new tracks preserves queue order."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        before_tracks = before_tracks + tuple(tracks)
        populated_queue.append_many(tracks)
        assert populated_queue.tracks == before_tracks

    def test_append_many_same_track(self, empty_queue, track):
        """Test: Able to append many of the same track to a queue."""
        duplicate_tracks: list[Track] = [track, track]
        empty_queue.append_many(duplicate_tracks)
        assert empty_queue.tracks == tuple(duplicate_tracks)
        assert len(empty_queue) == len(duplicate_tracks)

    def test_append_many_invalid_track_errors(self, empty_queue, track):
        """Test: Append many any invalid track raises TypeError."""
        with pytest.raises(TypeError):
            empty_queue.append_many([track, "NOT_A_TRACK"])

    def test_append_many_invalid_keeps_queue(self, populated_queue, track):
        """Test: If invalid tracks appended, queue is not affected."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(TypeError):
            populated_queue.append_many(track, "INVALID")
        assert populated_queue.tracks == before_tracks
        assert len(populated_queue) == len(before_tracks)


class TestPlaybackQueueInsertOneAt:
    def test_insert_one_at_0_empty_queue(self, empty_queue, track):
        """Test: Insert one track at index 0 of empty queue."""
        empty_queue.insert_one_at(0, track)
        assert len(empty_queue) == 1
        assert empty_queue.tracks[0] == track

    def test_insert_one_at_0_populated_queue(self, populated_queue, track):
        """Test: Insert one track at index 0 of populated queue."""
        before_len: int = len(populated_queue)
        populated_queue.insert_one_at(0, track)
        assert len(populated_queue) == before_len + 1
        assert populated_queue.tracks[0] == track

    def test_insert_one_at_mid_queue(self, populated_queue, track):
        """Test: Insert one track at the middle of a populated queue."""
        before_len: int = len(populated_queue)
        populated_queue.insert_one_at(1, track)
        assert len(populated_queue) == before_len + 1
        assert populated_queue.tracks[1] == track

    def test_insert_one_at_end_queue(self, populated_queue, track):
        """Test: Insert one track at the end of a populated queue."""
        before_len: int = len(populated_queue)
        populated_queue.insert_one_at(len(populated_queue), track)
        assert len(populated_queue) == before_len + 1
        assert populated_queue.tracks[-1] == track

    def test_insert_one_at_retains_order(self, populated_queue, track):
        """Test: Insert one track retains existing track order."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.insert_one_at(0, track)
        assert populated_queue.tracks[0] == track
        assert populated_queue.tracks[1:] == before_tracks

    def test_insert_one_at_duplicate_track(self, empty_queue, track):
        """Test: Insert one multiple times with the same track is okay."""
        empty_queue.insert_one_at(0, track)
        empty_queue.insert_one_at(0, track)
        assert len(empty_queue) == 2
        assert empty_queue.tracks[0] == track
        assert empty_queue.tracks[1] == track

    def test_insert_one_at_invalid_track(self, empty_queue):
        """Test: TypeError raised when inserting an invalid track."""
        with pytest.raises(TypeError):
            empty_queue.insert_one_at(0, "GOT_YA")

    def test_insert_one_at_index_negative(self, empty_queue, track):
        """Test: IndexError raised when inserting an index of negative value."""
        with pytest.raises(IndexError):
            empty_queue.insert_one_at(-1, track)

    def test_insert_one_at_index_too_big(self, empty_queue, track):
        """Test: IndexError raised when inserting an index too big."""
        with pytest.raises(IndexError):
            empty_queue.insert_one_at(len(empty_queue) +1, track)

    def test_insert_one_at_index_float(self, empty_queue, track):
        """Test: TypeError raised when inserting an index of float type."""
        with pytest.raises(TypeError):
            empty_queue.insert_one_at(0.0, track)

    def test_insert_one_at_index_string(self, empty_queue, track):
        """Test: TypeError raised when inserting an index of string type."""
        with pytest.raises(TypeError):
            empty_queue.insert_one_at("0", track)

    def test_insert_one_at_index_bool(self, empty_queue, track):
        """Test: TypeError raised when inserting an index of bool type."""
        with pytest.raises(TypeError):
            empty_queue.insert_one_at(True, track)
    
    def test_insert_one_at_fails_queue_still_okay(self, populated_queue):
        """Test: Insert one invalid operation leaves queue unchanged."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(TypeError):
            populated_queue.insert_one_at(0, "I_AM_A_TRACK")
        assert len(populated_queue) == len(before_tracks)
        assert populated_queue.tracks == before_tracks


"""
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