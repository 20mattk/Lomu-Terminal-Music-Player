import pytest
from lomu.library import Track, AudioFormat
from pathlib import Path
from datetime import datetime


# === TEST CASES ============================================================ #

class TestAudioFormat:
    def test_audioformat_valid_mp3_suffix_lowercase(self):
        """Test: AudioFormat can create a valid MP3 type from .mp3"""
        assert AudioFormat.from_suffix(".mp3") == AudioFormat.MP3

    def test_audioformat_valid_mp3_suffix_no_dot_lowercase(self):
        """Test: AudioFormat can create a valid MP3 type from mp3"""
        assert AudioFormat.from_suffix("mp3") == AudioFormat.MP3

    def test_audioformat_valid_mp3_suffix_uppercase(self):
        """Test: AudioFormat can create a valid MP3 type from .MP3"""
        assert AudioFormat.from_suffix(".MP3") == AudioFormat.MP3

    def test_audioformat_valid_mp3_suffix_no_dot_uppercase(self):
        """Test: AudioFormat can create a valid MP3 type from MP3"""
        assert AudioFormat.from_suffix("MP3") == AudioFormat.MP3

    def test_audioformat_valid_flac_suffix_lowercase(self):
        """Test: AudioFormat can create a valid FLAC type from .flac"""
        assert AudioFormat.from_suffix(".flac") == AudioFormat.FLAC

    def test_audioformat_valid_flac_suffix_no_dot_lowercase(self):
        """Test: AudioFormat can create a valid FLAC type from flac"""
        assert AudioFormat.from_suffix("flac") == AudioFormat.FLAC

    def test_audioformat_valid_flac_suffix_uppercase(self):
        """Test: AudioFormat can create a valid FLAC type from .FLAC"""
        assert AudioFormat.from_suffix(".FLAC") == AudioFormat.FLAC

    def test_audioformat_valid_flac_suffix_no_dot_uppercase(self):
        """Test: AudioFormat can create a valid FLAC type from FLAC"""
        assert AudioFormat.from_suffix("FLAC") == AudioFormat.FLAC

    def test_audioformat_valid_wav_suffix_lowercase(self):
        """Test: AudioFormat can create a valid WAV type from .wav"""
        assert AudioFormat.from_suffix(".wav") == AudioFormat.WAV

    def test_audioformat_valid_wav_suffix_no_dot_lowercase(self):
        """Test: AudioFormat can create a valid WAV type from wav"""
        assert AudioFormat.from_suffix("wav") == AudioFormat.WAV

    def test_audioformat_valid_wav_suffix_uppercase(self):
        """Test: AudioFormat can create a valid WAV type from .WAV"""
        assert AudioFormat.from_suffix(".WAV") == AudioFormat.WAV

    def test_audioformat_valid_wav_suffix_no_dot_uppercase(self):
        """Test: AudioFormat can create a valid WAV type from WAV"""
        assert AudioFormat.from_suffix("WAV") == AudioFormat.WAV

    def test_audioformat_invalid_audio_suffx(self):
        """Test: AudioFormat is unable to create from an unsupported type"""
        with pytest.raises(ValueError):
            AudioFormat.from_suffix(".ogg")

    def test_audioformat_empty_string_invalid_audio_suffix(self):
        """Test: AudioFormat is unable to create from an empty type"""
        with pytest.raises(ValueError):
            AudioFormat.from_suffix("")


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
            "duration": 305.2
        }
        defaults.update(kwargs)
        return Track(**defaults)

    def test_track_sets_audio_format(self):
        """Test: Track sets the correct AudioFormat"""
        track: Track = self.make_track()
        assert track.audio_format == AudioFormat.MP3

    def test_track_sets_valid_release_date_YYYYMMDD(self):
        """Test: Track sets a valid release date from YYYYMMDD"""
        track: Track = self.make_track()
        assert track.release_date == "2023-05-19"

    def test_track_sets_valid_release_date_YYYY(self):
        """Test: Track sets a valid release date from YYYY"""
        track: Track = self.make_track(release_date="2007")
        assert track.release_date == "2007-01-01"

    def test_track_sets_valid_release_date_YYMMDD(self):
        """Test: Track sets a valid relese date from YYMMDD"""
        track: Track = self.make_track(release_date="08-09-20")
        assert track.release_date == "2008-09-20"

    def test_track_adjusts_to_valid_release_date_YYYYMMDD(self):
        """Test: Track adjusts to valid release date from invalid YYYYMMDD"""
        track: Track = self.make_track(release_date="2009-18-20")
        assert track.release_date == "2009-01-01"

    def test_track_adjusts_to_valid_release_date_YYMMDD(self):
        """Test: Track adjusts to valid release date from invalid YYMMDD"""
        track: Track = self.make_track(release_date="09-18-78")
        assert track.release_date == "2009-01-01"

    def test_track_invalid_track_number(self):
        """Test: Track raises ValueError for invalid track number parsed"""
        with pytest.raises(ValueError):
            track: Track = self.make_track(track_number=0)

    def test_track_invalid_release_date(self):
        """Test: Track raises ValueError for invalid release date parsed"""
        with pytest.raises(ValueError):
            track: Track = self.make_track(release_date="February 18, 1987")

# =========================================================================== #
