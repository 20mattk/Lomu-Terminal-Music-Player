# === UPDATES =============================================================== #
# ON HOLD FOR DEVELOPMENT
# WILL REVIST ONCE MUSIC LIBRARY AND TRACKS FUNCTIONALITY IS COMPLETE
# THIS MIGHT BECOME A CHILD CLASS OF MUSIC LIBRARY CLASS


from .track import Track, AudioFormat
from uuid import UUID, uuid4


class Playlist:
    max_tracks: int = 200

    def __init__(self, name: str, description: str = "") -> None:
        self._id: UUID = uuid4()
        self.name: str = name
        self.description: str = description
        self._tracks: list[Track] = []
        # track_count: int      (computed below)
        # total_duration: float (computed below)

    # immutable properties
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def tracks(self) -> list[Track]:
        return list(self._tracks)

    # mutable properties
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Name cannot be empty or exceed 20 characters."""
        if not value or len(value) == 0:
            raise ValueError("Playlist name cannot be empty.")
        if len(value) > 20:
            raise ValueError("Playlist name cannot exceed 20 characters.")
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Description cannot exceed 50 characters."""
        if len(value) > 50:
            raise ValueError("Playlist description cannot exceed 50 characters.")
        self._description = value

    # computed properties
    @property
    def track_count(self) -> int:
        """Return the number of tracks in this playlist."""
        return len(self._tracks)

    @property
    def total_duration(self) -> float:
        """Return seconds duration of all tracks in this playlist."""
        return sum(track.duration for track in self._tracks)

    # mutation methods
    def add_track(self, track: Track) -> None:
        """
        Method to add a Track object to the playlist.

        Arguments:
            track (Track): The Track object to add to the playlist.

        Returns:
            None

        Raises:
            (ValueError): If the object being added is not of Track type.
            (ValueError): If the Track object already exists in the playlist.
        """
        if self.track_count == Playlist.max_tracks:
            raise ValueError(f"Cannot add more than {Playlist.max_tracks} tracks.")
        if not isinstance(track, Track):
            raise ValueError("Must add a Track object to the playlist.")
        if track in self._tracks:
            raise ValueError("That track already exists in the playlist.")
        self._tracks.append(track)

    def remove_track(self, track: Track) -> None:
        """
        Method to remove a specific Track object from the playlist.

        Arguments:
            track (Track): The Track object to remove from the playlist.

        Returns:
            None

        Raises:
            (ValueError): If the Track being removed cannot be found.
        """
        try:
            self._tracks.remove(track)
        except ValueError:
            raise ValueError("Could not find track to remove.")

    def remove_at(self, index: int) -> None:
        """
        Method to remove a Track from the playlist using its index.

        Arguments:
            index (int): Index of the Track object to remove from the playlist.

        Returns:
            None

        Raises:
            (IndexError): If the index is out of bounds for the playlist.
        """
        try:
            self._tracks.pop(index)
        except IndexError:
            raise IndexError(f"Index {index} is out of bounds for playlist")

    def clear_playlist(self) -> None:
        """
        Method to clear all Track objects from the playlist.

        Arguments:
            None

        Returns:
            None

        Raises:
            (ValueError): If something goes wrong with trying to clear.
        """
        try:
            self._tracks.clear()
        except Exception:
            raise ValueError("Could not clear the playlist.")

    # utility methods
    def __iter__(self):
        return iter(self._tracks)
