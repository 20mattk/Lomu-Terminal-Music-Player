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
        ),
        Track(
            file_path=Path("uhm.mp3"),
            title="Sure",
            artist="Yep",
            album="Kinda",
            release_date="1964",
            track_number=3,
            duration=104.0,
            album_art=b"\x89PNG\r\n\x1a\nMaybe"
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


class TestPlaybackQueueRemoveOneAt:
    def test_remove_one_at_queue_start(self, populated_queue):
        """Test: Remove one at the first track in the queue."""
        before_length: int = len(populated_queue)
        first_track: Track = populated_queue.tracks[0]
        removed_track: Track = populated_queue.remove_one_at(0)
        assert removed_track == first_track
        assert len(populated_queue) == before_length - 1

    def test_remove_one_at_queue_mid(self, populated_queue):
        """Test: Remove one at a mid point in the queue."""
        before_length: int = len(populated_queue)
        mid_track: Track = populated_queue.tracks[1]
        removed_track: Track = populated_queue.remove_one_at(1)
        assert removed_track == mid_track
        assert len(populated_queue) == before_length - 1

    def test_remove_one_at_queue_end(self, populated_queue):
        """Test: Remove one at the end point in the queue."""
        before_length: int = len(populated_queue)
        end_track: Track = populated_queue.tracks[-1]
        removed_track: Track = populated_queue.remove_one_at(
            len(populated_queue)-1
        )
        assert removed_track == end_track
        assert len(populated_queue) == before_length - 1

    def test_remove_one_at_single_track_queue(self, empty_queue, track):
        """Test: Remove one at of the only track in the queue."""
        empty_queue.append_one(track)
        empty_queue.remove_one_at(0)
        assert empty_queue.tracks == tuple()
        assert len(empty_queue) == 0

    def test_remove_one_at_track_is_returned(self, populated_queue):
        """Test: Remove one at returns the removed track."""
        before_track: Track = populated_queue.tracks[0]
        removed_track: Track = populated_queue.remove_one_at(0)
        assert removed_track == before_track

    def test_remove_one_at_track_retains_order(self, populated_queue):
        """Test: Remove one at retains the order of remaining tracks."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.remove_one_at(0)
        assert populated_queue.tracks == before_tracks[1:]

    def test_remove_one_at_float_index_is_error(self, populated_queue):
        """Test: Remove one at via float index raises TypeError."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(TypeError):
            populated_queue.remove_one_at(0.0)
        assert populated_queue.tracks == before_tracks

    def test_remove_one_at_string_index_is_error(self, populated_queue):
        """Test: Remove one at via string index raises TypeError."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(TypeError):
            populated_queue.remove_one_at("0")
        assert populated_queue.tracks == before_tracks

    def test_remove_one_at_bool_index_is_error(self, populated_queue):
        """Test: Remove one at via bool index raises TypeError."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(TypeError):
            populated_queue.remove_one_at(True)
        assert populated_queue.tracks == before_tracks

    def test_remove_one_at_negative_index_is_error(self, populated_queue):
        """Test: Remove one at via negative index raises IndexError."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(IndexError):
            populated_queue.remove_one_at(-1)
        assert populated_queue.tracks == before_tracks

    def test_remove_one_at_len_queue_index_is_error(self, populated_queue):
        """Test: Remove one at via len(queue) index raises IndexError."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(IndexError):
            populated_queue.remove_one_at(len(populated_queue))
        assert populated_queue.tracks == before_tracks

    def test_remove_one_at_len_queue_1_index_is_error(self, populated_queue):
        """Test: Remove one at via len(queue)+1 index raises IndexError."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(IndexError):
            populated_queue.remove_one_at(len(populated_queue)+1)
        assert populated_queue.tracks == before_tracks

    def test_remove_one_at_empty_queue_is_error(self, empty_queue):
        """Test: Remove one at from empty queue raises IndexError."""
        with pytest.raises(IndexError):
            empty_queue.remove_one_at(0)


class TestPlaybackQueueClearAll:
    def test_clear_all_populated_queue(self, populated_queue):
        """Test: Clear all tracks from a populated queue."""
        populated_queue.clear_all()
        assert populated_queue.tracks == tuple()
        assert len(populated_queue) == 0

    def test_clear_all_empty_queue(self, empty_queue):
        """Test: Clear all on an empty queue doesn't raise an error."""
        empty_queue.clear_all()
        assert empty_queue.tracks == tuple()
        assert len(empty_queue) == 0

    def test_clear_all_multiple_times(self, populated_queue):
        """Test: Clear all multiple times on a queue doesn't raise an error."""
        populated_queue.clear_all()
        assert populated_queue.tracks == tuple()
        assert len(populated_queue) == 0
        populated_queue.clear_all()
        assert populated_queue.tracks == tuple()
        assert len(populated_queue) == 0


class TestPlaybackQueuePopNext:
    def test_pop_next_first_track(self, populated_queue):
        """Test: Pop next the first track of a populated queue."""
        before_length: int = len(populated_queue)
        populated_queue.pop_next()
        assert len(populated_queue) == before_length - 1

    def test_pop_next_returns_track(self, populated_queue):
        """Test: Pop next returns the expected track from the queue."""
        before_track: Track = populated_queue.tracks[0]
        popped_track: Track = populated_queue.pop_next()
        assert popped_track == before_track

    def test_pop_next_retains_relative_order(self, populated_queue):
        """Test: Pop next retains relative order of original queue."""
        before_order: tuple[Track, ...] = populated_queue.tracks[1:]
        populated_queue.pop_next()
        assert populated_queue.tracks == before_order

    def test_pop_next_from_one_track_queue(self, empty_queue, track):
        """Test: Pop next works successfully on a one-track queue."""
        empty_queue.append_one(track)
        assert len(empty_queue) == 1
        assert empty_queue.tracks == (track,)
        empty_queue.pop_next()
        assert len(empty_queue) == 0
        assert empty_queue.tracks == tuple()

    def test_pop_next_empty_queue_is_error(self, empty_queue):
        """Test: Pop next raises IndexError when popping from empty queue."""
        with pytest.raises(IndexError):
            empty_queue.pop_next()


class TestPlaybackQueuePeekNext:
    def test_peek_next_first_track_returned(self, populated_queue):
        """Test: Peek next returns the first track of a populated queue."""
        before_track: Track = populated_queue.tracks[0]
        peeked_track: Track = populated_queue.peek_next()
        assert peeked_track == before_track

    def test_peek_next_retains_queue_order(self, populated_queue):
        """Test: Peek next retains order of populated queue."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.peek_next()
        assert populated_queue.tracks == before_tracks

    def test_peek_next_retains_queue_length(self, populated_queue):
        """Test: Peek next retains length of populated queue."""
        before_length: int = len(populated_queue)
        populated_queue.peek_next()
        assert len(populated_queue) == before_length

    def test_peek_next_one_track_queue(self, empty_queue, track):
        """Test: Peek next on a one-track queue."""
        empty_queue.append_one(track)
        assert len(empty_queue) == 1
        peeked_track: Track = empty_queue.peek_next()
        assert len(empty_queue) == 1
        assert peeked_track == track

    def test_peek_next_empty_queue_is_error(self, empty_queue):
        """Test: Peek next on empty queue raises IndexError."""
        with pytest.raises(IndexError):
            empty_queue.peek_next()

    def test_peek_next_returns_same_track_each_time(self, populated_queue):
        """Test: Peek next on the same unaltered queue returns same track."""
        peeked_track_1: Track = populated_queue.peek_next()
        peeked_track_2: Track = populated_queue.peek_next()
        assert peeked_track_1 == peeked_track_2


class TestPlaybackQueueMoveTrack:
    def test_move_track_first_to_end(self, populated_queue):
        """Test: Move track from first position to the end."""
        track_to_move: Track = populated_queue.tracks[0]
        populated_queue.move_track(0, len(populated_queue)-1)
        assert populated_queue.tracks[-1] == track_to_move

    def test_move_track_end_to_start(self, populated_queue):
        """Test: Move track from end position to the start."""
        track_to_move: Track = populated_queue.tracks[-1]
        populated_queue.move_track(len(populated_queue)-1, 0)
        assert populated_queue.tracks[0] == track_to_move

    def test_move_track_forward_one_spot(self, populated_queue):
        """Test: Move track forward one position."""
        track_to_move: Track = populated_queue.tracks[1]
        populated_queue.move_track(1, 0)
        assert populated_queue.tracks[0] == track_to_move

    def test_move_track_back_one_spot(self, populated_queue):
        """Test: Move track back one position."""
        track_to_move: Track = populated_queue.tracks[0]
        populated_queue.move_track(0, 1)
        assert populated_queue.tracks[1] == track_to_move

    def test_move_track_to_itself_unchanged(self, populated_queue):
        """Test: Move track to its own spot to verify queue is unchanged."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.move_track(0, 0)
        assert populated_queue.tracks == before_tracks

    def test_move_track_retains_other_relative_order(self, populated_queue):
        """Test: Move track leaves relative order of other tracks the same."""
        subset_tracks: tuple[Track, ...] = populated_queue.tracks[1:]
        populated_queue.move_track(0, len(populated_queue)-1)
        assert populated_queue.tracks[:-1] == subset_tracks

    def test_move_track_source_index_float(self, populated_queue):
        """Test: Move track raises TypeError when source index is float."""
        with pytest.raises(TypeError):
            populated_queue.move_track(0.0, 1)

    def test_move_track_destination_index_float(self, populated_queue):
        """Test: Move track raises TypeError when destination index is float."""
        with pytest.raises(TypeError):
            populated_queue.move_track(0, 1.0)

    def test_move_track_source_index_string(self, populated_queue):
        """Test: Move track raises TypeError when source index is string."""
        with pytest.raises(TypeError):
            populated_queue.move_track("0", 1)

    def test_move_track_destination_index_string(self, populated_queue):
        """Test: Move track raises TypeError when dest. index is string."""
        with pytest.raises(TypeError):
            populated_queue.move_track(0, "1")

    def test_move_track_source_index_bool(self, populated_queue):
        """Test: Move track raises TypeError when source index is bool."""
        with pytest.raises(TypeError):
            populated_queue.move_track(True, 1)

    def test_move_track_destination_index_bool(self, populated_queue):
        """Test: Move track raises TypeError when destination index is bool."""
        with pytest.raises(TypeError):
            populated_queue.move_track(0, True)

    def test_move_track_source_index_negative(self, populated_queue):
        """Test: Move track raises IndexError when source index is negative."""
        with pytest.raises(IndexError):
            populated_queue.move_track(-1, 1)

    def test_move_track_destination_index_negative(self, populated_queue):
        """Test: Move track raises IndexError when dest. index is negative."""
        with pytest.raises(IndexError):
            populated_queue.move_track(0, -1)

    def test_move_track_source_index_too_big(self, populated_queue):
        """Test: Move track raises IndexError when source index is too big."""
        with pytest.raises(IndexError):
            populated_queue.move_track(len(populated_queue), 1)

    def test_move_track_destination_index_too_big(self, populated_queue):
        """Test: Move track raises IndexError when dest. index is too big."""
        with pytest.raises(IndexError):
            populated_queue.move_track(0, len(populated_queue))

    def test_move_track_empty_queue_is_error(self, empty_queue):
        """Test: Move track raises IndexError when moving in empty queue."""
        with pytest.raises(IndexError):
            empty_queue.move_track(0, 1)

    def test_move_track_invalid_source_retains_queue(self, populated_queue):
        """Test: Move track invalid source index doesn't harm queue."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(IndexError):
            populated_queue.move_track(-1, 1)
        assert populated_queue.tracks == before_tracks

    def test_move_track_invalid_dest_retains_queue(self, populated_queue):
        """Test: Move track invalid dest. index doesn't harm queue."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        with pytest.raises(IndexError):
            populated_queue.move_track(1, -1)
        assert populated_queue.tracks == before_tracks


class TestPlaybackQueueShuffle:
    def test_shuffle_populated_queue_retains_length(self, populated_queue):
        """Test: Shuffle queue doesn't change the length of the queue."""
        before_length: int = len(populated_queue)
        populated_queue.shuffle()
        assert len(populated_queue) == before_length

    def test_shuffle_retains_all_original_tracks(self,  populated_queue):
        """Test: Shuffle a queue retains all tracks from original order."""
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.shuffle()
        for track in populated_queue.tracks:
            assert track in before_tracks

    def test_shuffle_with_duplicates_keeps_all(self, populated_queue):
        """Test: Shuffling queue with duplicate tracks keeps all counts."""
        duplicate_track: Track = populated_queue.tracks[0]
        populated_queue.append_one(duplicate_track)
        populated_queue.shuffle()
        duplicate_count: int = 0
        for track in populated_queue.tracks:
            if track == duplicate_track:
                duplicate_count += 1
        assert duplicate_count == 2

    def test_shuffle_empty_queue_no_error(self, empty_queue):
        """Test: Shuffling an empty queue raises no error."""
        empty_queue.shuffle()

    def test_shuffle_one_track_queue_successfully(self, empty_queue, track):
        """Test: Shuffling a one-track queue doesn't change the tracks."""
        empty_queue.append_one(track)
        before_queue: tuple[Track, ...] = empty_queue.tracks
        empty_queue.shuffle()
        assert empty_queue.tracks == before_queue

    def test_shuffle_multiple_times(self, populated_queue):
        """Test: Shuffling a queue multiple times doesn't lose tracks."""
        before_length: int = len(populated_queue)
        before_tracks: tuple[Track, ...] = populated_queue.tracks
        populated_queue.shuffle()
        populated_queue.shuffle()
        assert len(populated_queue) == before_length
        for track in populated_queue.tracks:
            assert track in before_tracks


"""
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