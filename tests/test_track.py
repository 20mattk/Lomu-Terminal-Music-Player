import pytest
from lomu.library import Track, AudioFormat
from pathlib import Path
from datetime import datetime


# === AudioFormat TESTS ===================================================== #

def test_audioformat_valid_mp3_suffix_lowercase():
    assert AudioFormat.from_suffix(".mp3") == AudioFormat.MP3


def test_audioformat_valid_mp3_suffix_no_dot_lowercase():
    assert AudioFormat.from_suffix("mp3") == AudioFormat.MP3


def test_audioformat_valid_mp3_suffix_uppercase():
    assert AudioFormat.from_suffix(".MP3") == AudioFormat.MP3


def test_audioformat_valid_mp3_suffix_no_dot_uppercase():
    assert AudioFormat.from_suffix("MP3") == AudioFormat.MP3


def test_audioformat_valid_flac_suffix_lowercase():
    assert AudioFormat.from_suffix(".flac") == AudioFormat.FLAC


def test_audioformat_valid_flac_suffix_no_dot_lowercase():
    assert AudioFormat.from_suffix("flac") == AudioFormat.FLAC


def test_audioformat_valid_flac_suffix_uppercase():
    assert AudioFormat.from_suffix(".FLAC") == AudioFormat.FLAC


def test_audioformat_valid_flac_suffix_no_dot_uppercase():
    assert AudioFormat.from_suffix("FLAC") == AudioFormat.FLAC


def test_audioformat_valid_wav_suffix_lowercase():
    assert AudioFormat.from_suffix(".wav") == AudioFormat.WAV


def test_audioformat_valid_wav_suffix_no_dot_lowercase():
    assert AudioFormat.from_suffix("wav") == AudioFormat.WAV


def test_audioformat_valid_wav_suffix_uppercase():
    assert AudioFormat.from_suffix(".WAV") == AudioFormat.WAV


def test_audioformat_valid_wav_suffix_no_dot_uppercase():
    assert AudioFormat.from_suffix("WAV") == AudioFormat.WAV


def test_audioformat_invalid_audio_suffx():
    with pytest.raises(ValueError):
        AudioFormat.from_suffix(".ogg")


def test_audioformat_empty_string_invalid_audio_suffix():
    with pytest.raises(ValueError):
        AudioFormat.from_suffix("")

# =========================================================================== #


# === Track TESTS =========================================================== #

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


def test_track_sets_audio_format():
    track: Track = make_track()
    assert track.audio_format == AudioFormat.MP3


def test_track_sets_valid_release_date_YYYYMMDD():
    track: Track = make_track()
    assert track.release_date == "2023-05-19"


def test_track_sets_valid_release_date_YYYY():
    track: Track = make_track(release_date="2007")
    assert track.release_date == "2007-01-01"


def test_track_sets_valid_release_date_YYMMDD():
    track: Track = make_track(release_date="08-09-20")
    assert track.release_date == "2008-09-20"


def test_track_adjusts_to_valid_release_date_YYYYMMDD():
    track: Track = make_track(release_date="2009-18-20")
    assert track.release_date == "2009-01-01"


def test_track_adjusts_to_valid_release_date_YYMMDD():
    track: Track = make_track(release_date="09-18-78")
    assert track.release_date == "2009-01-01"


def test_track_invalid_track_number():
    with pytest.raises(ValueError):
        track: Track = make_track(track_number=0)


def test_track_invalid_release_date():
    with pytest.raises(ValueError):
        track: Track = make_track(release_date="February 18, 1987")

# =========================================================================== #
