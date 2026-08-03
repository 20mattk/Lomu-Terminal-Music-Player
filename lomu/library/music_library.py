from .playlist import Playlist
from .track import Track, AudioFormat
from .metadata import load_track
from pathlib import Path


class MusicLibrary:
    def __init__(self, home_dir: Path):
        self._home_dir: Path = home_dir
        self._tracks: list[Track] = self.load_tracks_from_home_dir()
        self._playlists: list[Playlist] = []
        # track_count    (computed bleow)
        # total_duration (computed below)

    # computed properties
    @property
    def track_count(self) -> int:
        """Return the number of tracks in this library."""
        return len(self._tracks)

    @property
    def total_duration(self) -> float:
        """Return seconds duration of all tracks in this playlist."""
        return sum(track.duration for track in self._tracks)

    @property
    def playlist_count(self) -> int:
        """Return the number of playlists in this library."""
        return len(self._playlists)

    # mutable properties


    # library mutation methods
    def load_tracks_from_home_dir(self) -> list[Track]:
        """
        Load all files from the library's home directory into Track objects.
        Store them in the object's track list.

        Arguments:
            None

        Returns:
            all_track (list[Track]): The populated list of tracks.
        """
        all_file_paths: list[Path] = self.scan_home_dir()
        all_tracks: list[Track] = []

        for file_path in all_file_paths:
            try:
                all_tracks.append(load_track(file_path))
            except Exception as e:
                pass  # how to properly continue if file is of bad type?

        return all_tracks

    # remove_track
    # remove_at
    # clear_music_library

    # library utility methods
    def scan_home_dir(self) -> list[Path]:
        """Returns a list of all files in self._home_dir"""
        return [
            file_path
            for file_path in self._home_dir.rglob("*")
            if file_path.is_file()
        ]

    def __iter__(self):
        """Iterate over all tracks in self._tracks."""
        return iter(self._tracks)

    # playlist mutation methods
    # create_playlist
    # delete_playlist
