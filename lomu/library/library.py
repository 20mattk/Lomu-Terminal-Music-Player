# from .playlist import Playlist
from .track import Track, AudioFormat
from .metadata import load_track
from pathlib import Path
from collections.abc import Iterator


class Library:
    def __init__(self, home_dir: Path | str) -> None:
        self._home_dir: Path = Path(home_dir)
        self._tracks: list[Track] = []

    # === immutable properties === #
    @property
    def home_dir(self) -> Path:
        """Return the Path of the home directory."""
        return self._home_dir

    @property
    def tracks(self) -> tuple[Track, ...]:
        """Return an immutable Tuple of the library's tracks."""
        return tuple(self._tracks)

    # === computed properties === #
    @property
    def total_duration(self) -> float:
        """Return seconds duration of all tracks in this playlist."""
        return sum(track.duration for track in self._tracks)

    # === utility methods === #
    def populate_library(self) -> None:
        """
        Load all files from the library's home directory into Track objects.
        Store them in the object's track list.
        A rescan will fully replace the existing library.
        """
        loaded_tracks: list[Track] = []

        for file_path in self.scan_home_dir():
            try:
                track: Track = load_track(file_path)
            except FileNotFoundError as f:
                continue
            except ValueError as v:
                continue

            loaded_tracks.append(track)

        self._tracks = loaded_tracks

    def clear_library(self) -> None:
        """Clears all tracks from the library."""
        self._tracks.clear()

    def scan_home_dir(self) -> list[Path]:
        """
        Returns a list of all files in self._home_dir.

        Returns:
            (list[Path]): A list of all audio file file paths.

        Raises:
            (FileNotFoundError): If supplied path is not reachable.
            (NotADirectoryError): If supplied path isn't a directory.
        """
        if not self._home_dir.exists():
            raise FileNotFoundError(
                f"Library path does not exist: {self._home_dir}"
            )

        if not self._home_dir.is_dir():
            raise NotADirectoryError(
                f"Library path is not a directory: {self._home_dir}"
            )

        supported_formats: set[str] = {
            audio_format.value for audio_format in AudioFormat
        }

        return [
            file_path for file_path in self._home_dir.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() in supported_formats
        ]

    # === dunder methods === #
    def __len__(self) -> int:
        """Return the number of tracks in the library."""
        return len(self._tracks)

    def __iter__(self) -> Iterator[Track]:
        """Iterate over all tracks in self._tracks."""
        return iter(self._tracks)
