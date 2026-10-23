# from .playlist import Playlist
from .track import Track, AudioFormat
from .metadata import load_track
from pathlib import Path


class Library:
    def __init__(self, home_dir: Path):
        self._home_dir: Path = home_dir
        self._tracks: list[Track] = []

    # === immutable properties === #
    @property
    def home_dir(self) -> Path:
        """Return the Path of the home directory."""
        return self._home_dir

    @property
    def tracks(self) -> tuple[Track, ...]:
        """Return all Tracks in the library as an ummutable Tuple."""
        return tuple(self._tracks)

    # === computed properties === #
    @property
    def track_count(self) -> int:
        """Return the number of tracks in this library."""
        return len(self._tracks)

    @property
    def total_duration(self) -> float:
        """Return seconds duration of all tracks in this playlist."""
        return sum(track.duration for track in self._tracks)

    # === utility methods === #
    def populate_library(self) -> None:
        """
        Load all files from the library's home directory into Track objects.
        Store them in the object's track list.
        """
        loaded_tracks: list[Track] = []

        for file_path in self.scan_home_dir():
            try:
                track: Track = load_track(file_path)
            except FileNotFoundError as f:
                print(f"Skipping {file_path}. Could not be found. {f}")
                continue
            except ValueError as v:
                print(f"Skipping {file_path}. Invalid format. {v}")
                continue

            loaded_tracks.append(track)

        self._tracks = loaded_tracks

    def clear_library(self) -> None:
        """Clears all tracks and playlists from the library."""
        self._tracks.clear()

    # library utility methods
    def scan_home_dir(self) -> list[Path]:
        """
        Returns a list of all files in self._home_dir.

        Returns:
            (list[Path]): A list of all audio file file paths.

        Raises:
            (PermissionError): If the user isn't able to access the directory.
            (Exception): A generic error to catch any other issues.
        """
        if not self._home_dir.is_dir():
            raise NotADirectoryError(self._home_dir)

        supported_formats: set[str] = {
            audio_format.value for audio_format in AudioFormat
        }

        return [
            file_path for file_path in self._home_dir.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() in supported_formats
        ]

    def __iter__(self):
        """Iterate over all tracks in self._tracks."""
        return iter(self._tracks)
