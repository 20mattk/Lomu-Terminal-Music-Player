import pytest
from pathlib import Path
from lomu.library import Library


# === TEST CASES ============================================================ #

class TestLibraryInitialization:
    def test_library_initialization_instance(self):
        """Test: Initialized library is of Library type"""
        assert isinstance(Library(Path("/")), Library)

    def test_initialized_track_count(self):
        """Test: Affirm a newly-initialized library has 0 tracks"""
        assert Library(Path("/")).track_count == 0

    def test_initialized_duration(self):
        """Test: Affirm a newly-initialized library has 0.0 duration"""
        assert Library(Path("/")).total_duration == 0.0

    def test_initialized_track_list(self):
        """Test: Affirm a newly-initialized library has empty track list"""
        assert Library(Path("/")).tracks == []

    def test_initialized_home_dir(self):
        """Test: Affirm a newly-initialized library has Path type home_dir"""
        assert isinstance(Library(Path("/")).home_dir, Path)


class TestFileScanning:
    def test_scanning_returns_paths(self):
        """Test: scan_home_dir returns a list of Path objects"""
        file_paths: list[Path] = Library(
            Path("./tests/Audio")
        ).scan_home_dir()
        assert all(isinstance(file, Path) for file in file_paths)

    def test_scanning_empty_path(self):
        """Test: scan_home_dir returns nothing when it doesn't find audio"""
        file_paths: list[Path] = Library(Path("~")).scan_home_dir()
        assert len(file_paths) == 0


class TestLibraryPopulation:
    def test_library_population(self):
        """Test: Adding tracks successfully populates the library"""
        library: Library = Library(Path("./tests/Audio"))
        library.populate_library()
        assert library.track_count > 0


class TestLibraryCleaning:
    def test_library_cleans_tracks(self):
        """Test: Clearing a populated library clears track list"""
        library: Library = Library(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.tracks == []

    def test_library_cleans_track_count(self):
        """Test: Clearing a populated library resets track count"""
        library: Library = Library(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.track_count == 0

    def test_library_cleans_duration(self):
        """Test: Clearing a populated library resets total duration"""
        library: Library = Library(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.total_duration == 0.0

    def test_library_cleans_leaves_home_dir(self):
        """Test: Clearing a populated library doesn't touch home_dir"""
        library: Library = Library(Path("./tests/Audio"))
        library.populate_library()
        library.clear_library()
        assert library.home_dir != None and library.home_dir != ""
