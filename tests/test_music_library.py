import pytest
from pathlib import Path
from lomu.library import MusicLibrary


# === FIXTURES ============================================================== #


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
        file_paths: list[Path] = MusicLibrary(Path("./Audio/")).scan_home_dir()
        assert all(isinstance(file, Path) for file in file_paths)

    def test_scanning_empty_path(self):
        """Test: scan_home_dir returns nothing when it doesn't find audio"""
        file_paths: list[Path] = MusicLibrary(Path("~")).scan_home_dir()
        assert len(file_paths) == 0


class TestLibraryPopulation:
    pass
    # create mock track, call populate_library, self.tracks contains it now
    # test invalid format correctly identified with mock track that's "bad"


class TestLibraryCleaning:
    pass
    # tracks becomes empty
    # track_count == 0
    # total_duration == 0.0
    # home_dir is still populated
