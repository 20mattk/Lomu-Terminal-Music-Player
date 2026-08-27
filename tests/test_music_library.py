import pytest
from pathlib import Path
from lomu.library import MusicLibrary


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


# === TEST CASES ============================================================ #

class TestLibraryInitialization:
    def test_musiclibrary_initialization_instance(self):
        """Test: Initialized library is of MusicLibrary type"""
        assert isinstance(MusicLibrary(Path("/")), MusicLibrary)

    def test_initialized_track_count(self):
        """Test: Affirm a newly-initialized library has 0 tracks"""
        assert MusicLibrary(Path("/")).track_count == 0

    def test_initialized_duration(self):
        """Test: Affirm a newly-initialized library has 0.0 duration"""
        assert MusicLibrary(Path("/")).total_duration == 0.0

    def test_initialized_track_list(self):
        """Test: Affirm a newly-initialized library has empty track list"""
        assert MusicLibrary(Path("/")).tracks == []

    def test_initialized_home_dir(self):
        """Test: Affirm a newly-initialized library has Path type home_dir"""
        assert isinstance(MusicLibrary(Path("/")).home_dir, Path)


class TestFileScanning:
    def test_scanning_returns_paths(self):
        """Test: scan_home_dir returns a list of Path objects"""
        file_paths: list[Path] = MusicLibrary(
            Path("./tests/Audio")
        ).scan_home_dir()
        assert all(isinstance(file, Path) for file in file_paths)

    def test_scanning_empty_path(self):
        """Test: scan_home_dir returns nothing when it doesn't find audio"""
        file_paths: list[Path] = MusicLibrary(Path("~")).scan_home_dir()
        assert len(file_paths) == 0


class TestLibraryPopulation:
    def test_library_population(self):
        """Test: Adding tracks successfully populates the library"""
        library: MusicLibrary = MusicLibrary(Path("./tests/Audio"))
        library.populate_library()
        assert library.track_count > 0


class TestLibraryCleaning:
    def test_library_cleans_tracks(self):
        """Test: Clearing a populated library clears track list"""
        library: MusicLibrary = MusicLibrary(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.tracks == []

    def test_library_cleans_track_count(self):
        """Test: Clearing a populated library resets track count"""
        library: MusicLibrary = MusicLibrary(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.track_count == 0

    def test_library_cleans_duration(self):
        """Test: Clearing a populated library resets total duration"""
        library: MusicLibrary = MusicLibrary(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.total_duration == 0.0

    def test_library_cleans_leaves_home_dir(self):
        """Test: Clearing a populated library doesn't touch home_dir"""
        library: MusicLibrary = MusicLibrary(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.home_dir != None and library.home_dir != ""
