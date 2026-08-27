# Group 1: Initialization & Computed Properties
#    1. Check initial value of track_count

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
    pass
    # scan_home_dir gets a list of valid Path objects
    # scan_home_dir rightfully gets denied permission to scan a directory
    # scan_home_dir rightfully raises an error when scanning goes wrong?


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
