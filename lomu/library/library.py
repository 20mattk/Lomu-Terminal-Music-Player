# NOTICE: Playlist development is on hold for now


# from .playlist import Playlist
from .track import Track, AudioFormat
from .metadata import load_track
from pathlib import Path


class Library:
    def __init__(self, home_dir: Path):
        self._home_dir: Path = home_dir
        self._tracks: list[Track] = []
        # self._playlists: list[Playlist] = []
        # track_count    (computed bleow)
        # total_duration (computed below)

    # immutable properties
    @property
    def home_dir(self) -> Path:
        """Return the Path of the home directory."""
        return self._home_dir

    @property
    def tracks(self) -> list[Track]:
        """Return the list of Track objects in the library."""
        return list(self._tracks)

    # @property
    # def playlists(self) -> list[Playlist]:
    #     """Return the list of all Playlist objects in the library."""
    #     return list(self._playlists)

    # computed properties
    @property
    def track_count(self) -> int:
        """Return the number of tracks in this library."""
        return len(self._tracks)

    @property
    def total_duration(self) -> float:
        """Return seconds duration of all tracks in this playlist."""
        return sum(track.duration for track in self._tracks)

    # @property
    # def playlist_count(self) -> int:
    #     """Return the number of playlists in this library."""
    #     return len(self._playlists)

    # library mutation methods
    def populate_library(self) -> list[Track]:
        """
        Load all files from the library's home directory into Track objects.
        Store them in the object's track list.

        Arguments:
            None

        Returns:
            None

        Raises:
            None
        """
        all_file_paths: list[Path] = self.scan_home_dir()

        for file_path in all_file_paths:
            try:
                self._tracks.append(load_track(file_path))
            except ValueError as v:
                print(f"Skipping {file_path}. Invalid format. {v}")
            except Exception as e:
                print(f"Skipping {file_path}. Unexpected loading error. {e}")

    def clear_library(self) -> None:
        """
        Clears all tracks and playlists from the library.

        Arguments:
            None

        Returns:
            None

        Raises:
            None
        """
        self._tracks.clear()
        # self._playlists.clear()

    # library utility methods
    def scan_home_dir(self) -> list[Path]:
        """
        Returns a list of all files in self._home_dir.

        Arguments:
            None

        Returns:
            (list[Path]): A list of all audio file file paths.

        Raises:
            (PermissionError): If the user isn't able to access the directory.
            (Exception): A generic error to catch any other issues.
        """
        try:
            return [
                file_path
                for file_path in self._home_dir.rglob("*")
                if file_path.is_file()
            ]
        except PermissionError as p:
            print(f"Access denied for {self._home_dir}. {p}")
            raise PermissionError(f"Access denied for {self._home_dir}") from e
        except Exception as e:
            print(f"Error in trying to scan the directory {self._home_dir}")
            raise

    def __iter__(self):
        """Iterate over all tracks in self._tracks."""
        return iter(self._tracks)

    # # playlist mutation methods
    # def create_playlist(self, name: str, description: str = "") -> None:
    #     """
    #     Create a playlist and add it to the library.

    #     Arguments:
    #         name (str): The name to give to the playlist.
    #         description (str): The description to give to the playlist.

    #     Returns:
    #         None

    #     Raises:
    #         None
    #     """
    #     try:
    #         playlist: Playlist = Playlist(name, description)
    #     except ValueError as v:
    #         print(f"Unable to create the playlist: {v}.")
    #         return

    #     self._playlists.append(playlist)

    # def delete_playlist(self, playlist_id: UUID) -> None:
    #     """
    #     Delete a playlist from the music library, using its ID.

    #     Arguments:
    #         playlist_id (UUID): The ID of the playlist to delete.

    #     Returns:
    #         None

    #     Raises:
    #         (ValueError): If the playlist to delete cannot be found.
    #     """
    #     idx_to_del: int = next(
    #         (i for i, p in enumerate(self._playlists) if p.id == playlist_id),
    #         None
    #     )

    #     if idx_to_del is None:
    #         raise ValueError(f"Playlist ({playlist_id}) is not found.")

    #     self._playlist.pop(idx_to_del)
