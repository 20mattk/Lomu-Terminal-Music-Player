import pytest
from pathlib import Path
from lomu.library import Playlist, Track, AudioFormat
from uuid import UUID, uuid4


# === FIXTURES ============================================================== #

@pytest.fixture
def test_track_1() -> Track:
    """Fixture to create a basic Track object"""
    return Track(
        file_path=Path("test_track_1.flac"),
        title="Test Track 1 Title",
        artist="Test Track 1 Artist",
        album="Test Track 1 Album",
        release_date="2024-08-19",
        track_number=3,
        duration=201.542
    )


@pytest.fixture
def test_track_2() -> Track:
    """Fixture to create a basic Track object"""
    return Track(
        file_path=Path("test_track_2.mp3"),
        title="Test Track 2 Title",
        artist="Test Track 2 Artist",
        album="Test Track 2 Album",
        release_date="1985-03-19",
        track_number=8,
        duration=164.202
    )


@pytest.fixture
def empty_playlist() -> Playlist:
    """Fixture to create a basic Playlist object"""
    return Playlist(
        name="Playlist Title",
        description="Playlist description for empty_playlist fixture."
    )


@pytest.fixture
def nonempty_playlist(test_track_1, test_track_2) -> Playlist:
    """Fixture to create a non-empty Playlist object"""
    playlist: Playlist = Playlist(
        name="Playlist Title",
        description="Playlist description of nonempty_playlist fixture."""
    )

    playlist.add_track(test_track_1)
    playlist.add_track(test_track_2)

    return playlist

# =========================================================================== #


# === TEST CASES ============================================================ #

class TestPlaylistInitialization:
    def test_initialization_instance(self):
        """Test: Initialized playlist object is of Playlist type"""
        assert isinstance(Playlist("Test Playlist"), Playlist)


class TestPlaylistID:
    def test_playlist_id_initialization(self):
        """Test: Initialized playlist ID is of UUID type"""
        assert isinstance(Playlist("Test Playlist").id, UUID)


class TestPlaylistName:
    def test_playlist_name_initialization(self):
        """Test: Playlist name is what it should be"""
        assert Playlist("Test Playlist").name == "Test Playlist"

    def test_playlist_no_name_raises_error(self):
        """Test: Playlist initialized without a name raises TypeError"""
        with pytest.raises(TypeError):
            Playlist()


class TestPlaylistDescription:
    def test_default_description(self):
        """Test: Playlist description initializes to blank by default"""
        assert Playlist("Test Playlist").description == ""

    def test_user_set_description(self):
        """Test: User-defined description is properly set"""
        assert Playlist("Name", "Description").description == "Description"


class TestPlaylistComputedProperties:
    def test_playlist_track_count_0(self):
        """Test: A newly-initialized playlist object has 0 tracks"""
        assert Playlist("Test Playlist").track_count == 0

    def test_playlist_total_duration_0(self):
        """Test: A newly-initialized playlist object has 0.0 mins duration"""
        assert Playlist("Test Playlist").total_duration == 0.0


class TestPlaylistTrackManagement:
    def test_playlist_add_track(self, empty_playlist, test_track_1):
        """Test: Adding a Track object to a Playlist object is successful"""
        empty_playlist.add_track(test_track_1)
        assert empty_playlist.track_count == 1
        assert empty_playlist.total_duration > 0.0
        assert empty_playlist.total_duration == pytest.approx(
            test_track_1.duration
        )

    def test_playlist_add_duplicate_track(self, empty_playlist, test_track_1):
        """Test: Adding a duplicate Track to a playlist throws a ValueError"""
        empty_playlist.add_track(test_track_1)
        with pytest.raises(ValueError):
            empty_playlist.add_track(test_track_1)

    def test_playlist_add_non_track(self, empty_playlist, test_track_1):
        """Test: Adding a non-Track object raises a ValueError"""
        for not_a_track in ["Not a Track", 10, 80.34, dict(), list()]:
            with pytest.raises(ValueError):
                empty_playlist.add_track(not_a_track)

    def test_playlist_remove_track(self, nonempty_playlist, test_track_1):
        """Test: Removing a Track object is done successfully"""
        initial_track_count: int = nonempty_playlist.track_count
        initial_total_duration: float = nonempty_playlist.total_duration
        nonempty_playlist.remove_track(test_track_1)
        assert nonempty_playlist.track_count == initial_track_count - 1
        assert nonempty_playlist.total_duration < initial_total_duration

    def test_playlist_remove_non_track(self, nonempty_playlist, test_track_1):
        """Test: Removing a non-Track object rases a ValueError"""
        for not_a_track in ["Not a Track", 10, 80.34, dict(), list()]:
            with pytest.raises(ValueError):
                nonempty_playlist.remove_track(not_a_track)

    def test_playlist_remove_at(self, nonempty_playlist):
        """Test: Removing at a valid index performs successfully"""
        initial_track_count: int = nonempty_playlist.track_count
        initial_total_duration: float = nonempty_playlist.total_duration
        nonempty_playlist.remove_at(1)
        assert nonempty_playlist.track_count == initial_track_count - 1
        assert nonempty_playlist.total_duration < initial_total_duration

    def test_playlist_remove_at_invalid(self, nonempty_playlist):
        """Test: Removing at an invalid index raises ValueError"""
        with pytest.raises(IndexError):
            nonempty_playlist.remove_at(5)

    def test_playlist_clear(self, nonempty_playlist):
        """Test: Clearing a playlist performs successfully"""
        nonempty_playlist.clear_playlist()
        assert nonempty_playlist.track_count == 0
        assert nonempty_playlist.total_duration == 0.0


class TestPlaylistIteration:
    def test_playlist_iteration_works(self, nonempty_playlist):
        """Test: Ensure iteration through a Playlist object works"""
        tracks_iterated: int = 0
        for track in nonempty_playlist:
            assert isinstance(track, Track)
            tracks_iterated += 1
        assert nonempty_playlist.track_count == tracks_iterated

# =========================================================================== #
