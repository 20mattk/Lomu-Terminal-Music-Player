import pytest
from lomu.library import Track, AudioFormat, load_track
from pathlib import Path
import git


# === FIXTURES ============================================================== #

@pytest.fixture
def git_repo() -> Path:
    git_repo_obj = git.Repo('.', search_parent_directories=True)
    return Path(git_repo_obj.working_tree_dir)


@pytest.fixture
def test_mp3_real_path(git_repo) -> Path:
    return git_repo / Path("tests/Audio/12 - Euclid.mp3")


@pytest.fixture
def test_flac_real_path(git_repo) -> Path:
    return git_repo / Path("tests/Audio/07 - Down.flac")


@pytest.fixture
def test_wav_real_path(git_repo) -> Path:
    return git_repo / Path("tests/Audio/01 - Oh Well, Oh Well.wav")


@pytest.fixture
def test_mp3_expected_track(test_mp3_real_path) -> Track:
    return Track(
        file_path=test_mp3_real_path,
        title="Euclid",
        artist="Sleep Token",
        album="Take Me Back To Eden",
        release_date="2023-01-01",
        track_number=12,
        duration=313.3910204081633
        # album_art not included in testing
        # audio_format is automatically computed
    )


@pytest.fixture
def test_flac_expected_track(test_flac_real_path) -> Track:
    return Track(
        file_path=test_flac_real_path,
        title="Down",
        artist="blink-182",
        album="blink-182",
        release_date="2003-11-15",
        track_number=7,
        duration=193.01333333333332
        # album_art not included in testing
        # audio_format is automatically computed
    )


@pytest.fixture
def test_wav_expected_track(test_wav_real_path) -> Track:
    return Track(
        file_path=test_wav_real_path,
        title="Oh Well, Oh Well",
        artist="Mayday Parade",
        album="Mayday Parade",
        release_date="2011-11-20",
        track_number=1,
        duration=289.8701587301587
        # album_art not included in testing
        # audio_format is automatically computed
    )

# =========================================================================== #


# === TEST CASES ============================================================ #

def test_load_mp3_file(test_mp3_real_path, test_mp3_expected_track) -> None:
    mp3_track: Track = load_track(test_mp3_real_path)

    assert isinstance(mp3_track, Track)
    assert mp3_track.file_path == test_mp3_expected_track.file_path
    assert mp3_track.title == test_mp3_expected_track.title
    assert mp3_track.artist == test_mp3_expected_track.artist
    assert mp3_track.album == test_mp3_expected_track.album
    assert mp3_track.release_date == test_mp3_expected_track.release_date
    assert mp3_track.track_number == test_mp3_expected_track.track_number
    assert mp3_track.duration == test_mp3_expected_track.duration
    assert mp3_track.audio_format == test_mp3_expected_track.audio_format


def test_load_flac_file(test_flac_real_path, test_flac_expected_track) -> None:
    flac_track: Track = load_track(test_flac_real_path)

    assert isinstance(flac_track, Track)
    assert flac_track.file_path == test_flac_expected_track.file_path
    assert flac_track.title == test_flac_expected_track.title
    assert flac_track.artist == test_flac_expected_track.artist
    assert flac_track.album == test_flac_expected_track.album
    assert flac_track.release_date == test_flac_expected_track.release_date
    assert flac_track.track_number == test_flac_expected_track.track_number
    assert flac_track.duration == test_flac_expected_track.duration
    assert flac_track.audio_format == test_flac_expected_track.audio_format


def test_wav_flac_file(test_wav_real_path, test_wav_expected_track) -> None:
    wav_track: Track = load_track(test_wav_real_path)

    assert isinstance(wav_track, Track)
    assert wav_track.file_path == test_wav_expected_track.file_path
    assert wav_track.title == test_wav_expected_track.title
    assert wav_track.artist == test_wav_expected_track.artist
    assert wav_track.album == test_wav_expected_track.album
    assert wav_track.release_date == test_wav_expected_track.release_date
    assert wav_track.track_number == test_wav_expected_track.track_number
    assert wav_track.duration == test_wav_expected_track.duration
    assert wav_track.audio_format == test_wav_expected_track.audio_format

# =========================================================================== #
