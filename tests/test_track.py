import pytest
from lomu.library import Track, AudioFormat
from pathlib import Path
from datetime import datetime


# === TEST CASES ============================================================ #

class TestAudioFormat:
    @pytest.mark.parametrize("input_ext, expected_format, error", [
        # Success Test 1: Create valid MP3 type from .mp3
        (".mp3", AudioFormat.MP3, None),

        # Success Test 2: Create valid MP3 type from mp3
        ("mp3", AudioFormat.MP3, None),

        # Success Test 3: Create valid MP3 type from .MP3
        (".MP3", AudioFormat.MP3, None),

        # Success Test 4: Create valid MP3 type from MP3
        ("MP3", AudioFormat.MP3, None),

        # Success Test 5: Create valid FLAC type from .flac
        (".flac", AudioFormat.FLAC, None),

        # Success Test 6: Create valid FLAC type from flac
        ("flac", AudioFormat.FLAC, None),

        # Success Test 7: Create valid FLAC type from .FLAC
        (".FLAC", AudioFormat.FLAC, None),

        # Success Test 8: Create valid FLAC type from FLAC
        ("FLAC", AudioFormat.FLAC, None),

        # Success Test 9: Create valid WAV type from .wav
        (".wav", AudioFormat.WAV, None),

        # Success Test 10: Create valid WAV type from wav
        ("wav", AudioFormat.WAV, None),

        # Success Test 11: Create valid WAV type from .WAV
        (".WAV", AudioFormat.WAV, None),

        # Success Test 12: Create valid WAV type from WAV
        ("WAV", AudioFormat.WAV, None),

        # Failure Test 1: ValueError raised from .ogg input
        (".ogg", None, ValueError),

        # Failure Test 2: ValueError raised from blank input
        ("", None, ValueError)
    ])

    def test_audioformat_handle_input(self, input_ext, expected_format, error):
        """Test: Tests various extension inputs to create an AudioFormat"""
        if error is None:
            assert AudioFormat.from_suffix(input_ext) == expected_format
        else:
            with pytest.raises(ValueError):
                AudioFormat.from_suffix(input_ext)


class TestTrack:
    @staticmethod
    def make_track(**kwargs):
        defaults = {
            "file_path": Path("song.mp3"),
            "title": "Song",
            "artist": "Artist",
            "album": "Album",
            "release_date": "2023-05-19",
            "track_number": 12,
            "duration": 305.2,
            "album_art": b"\x89PNG\r\n\x1a\nAlbumArtImage"
        }
        defaults.update(kwargs)
        return Track(**defaults)

    @pytest.mark.parametrize("input_date, normalized_date, error", [
        # Success Test 1: Valid Release Date from YYYYMMDD
        ("2023-05-19", "2023-05-19", None),

        # Success Test 2: Valid Release Date from YYYY
        ("2007", "2007-01-01", None),

        # Success Test 3: Valid Release Date from YYMMDD
        ("08-09-20", "2008-09-20", None),

        # Success Test 4: Valid Release Date from Invalid YYYYMMDD
        ("2009-18-20", "2009-01-01", None),

        # Success Test 5: Valid Release Date from Invalid YYMMDD
        ("09-18-78", "2009-01-01", None),

        # Failure Test 1: Invalid release date raises an error when parsed
        ("February, 18, 1987", None, ValueError)
    ])

    def test_track_handles_dates(self, input_date, normalized_date, error):
        """Test: Various date str inputs produce valid date normalizations"""
        if error is None:
            track: Track = self.make_track(release_date=input_date)
            assert track.release_date == normalized_date
        else:
            with pytest.raises(ValueError):
                track: Track = self.make_track(release_date=input_date)

    def test_track_sets_audio_format(self):
        """Test: Track sets the correct AudioFormat"""
        track: Track = self.make_track()
        assert track.audio_format == AudioFormat.MP3

    def test_track_invalid_track_number(self):
        """Test: Track raises ValueError for invalid track number parsed"""
        with pytest.raises(ValueError):
            track: Track = self.make_track(track_number=0)

    def test_track_creates_valid_album_art(self):
        """Test: Track creates valid album art when supplied with data"""
        track: Track = self.make_track()
        assert track.album_art == b"\x89PNG\r\n\x1a\nAlbumArtImage"

    def test_track_creates_without_album_art(self):
        """Test: Track still creates without album art supplied"""
        track: Track = self.make_track(album_art=None)
        assert track.album_art == None

# =========================================================================== #
