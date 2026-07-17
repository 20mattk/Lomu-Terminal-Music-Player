import pytest
from lomu.library import Playlist
from uuid import UUID, uuid4
from unittest.mock import Mock


# === FIXTURES ============================================================== #

@pytest.fixture
def mock_track_1():
    class MockTrack:
        def __init__(self, duration):
            self.duration = duration
    return MockTrack(duration=180.5)


@pytest.fixture
def mock_track_2():
    class MockTrack:
        def __init__(self, album):
            self.album = album
    return MockTrack(album="Test Album")


@pytest.fixture
def valid_playlist(mock_track_1, mock_track_2):
    playlist = Playlist("Test Name", "Test description.")
    playlist.add_track(mock_track_1)
    playlist.add_track(mock_track_2)
    return playlist


# === TEST CASES ============================================================ #

class TestPlaylistInitialization:
    def test_initialization_instance(self):
        assert isinstance(Playlist("Test Playlist"), Playlist)


class TestPlaylistID:
    def test_playlist_id_initialization(self):
        assert isinstance(Playlist("Test Playlist").id, UUID)


class TestPlaylistName:
    def test_playlist_name_initialization(self):
        assert Playlist("Test Playlist").name == "Test Playlist"

    def test_playlist_no_name_raises_error(self):
        with pytest.raises(TypeError):
            Playlist()


class TestPlaylistDescription:
    def test_default_description(self):
        assert Playlist("Test Playlist").description == ""


class TestPlaylistComputedProperties:
    def test_playlist_track_count_0(self):
        assert Playlist("Test Playlist").track_count == 0

    def test_playlist_total_duration_0(self):
        assert Playlist("Test Playlist").total_duration == 0.0


class TestPlaylistTrackManagement:
    pass
