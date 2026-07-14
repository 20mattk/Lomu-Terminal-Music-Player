from .track import Track, AudioFormat
from uuid import UUID, uuid4


class Playlist:
    def __init__(self, name: str, description: str = "") -> None:
        self._id: UUID = uuid4()
        self._name: str = name
        self._description: str = description
        self._tracks: list[Track] = []
        # track_count    (computed below)
        # total_duration (computed below)

    # immutable properties
    @property
    def id(self) -> UUID:
        """Return the unique ID of this playlist."""
        return self._id

    # mutable properties
    @property
    def name(self) -> str:
        """Return the name of the playlist."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Setter for the playlist name. Must follow naming rules.

        Arguments:
            value (str): The value to name the playlist.

        Returns:
            None

        Raises:
            (ValueError): If the playlist name is empty.
            (ValueError): If the playlist name is beyond 20 characters long.
        """
        if not value or len(value) == 0:
            raise ValueError("Playlist name cannot be empty.")
        if len(value) > 20:
            raise ValueError("Playlist name cannot exceed 20 characters.")
        self._name = value

    @property
    def description(self) -> str:
        """Return the description of the playlist."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Setter for the playlist description. Must follow naming rules.

        Arguments:
            value (str): The value to give the playlist description.

        Returns:
            None

        Raises:
            (ValueError): If the playlist description is over 50 characters.
        """
        if len(value) > 50:
            raise ValueError("Playlist name cannot exceed 50 characters.")
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
        """
        if track in self._tracks:
            raise ValueError("That track already exists in the playlist.")
        if isinstance(track, Track):
            self._tracks.append(track)
        else:
            raise ValueError("Must add a Track object to the playlist.")

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
            (ValueError): If the index is out of bounds for the playlist.
        """
        try:
            self._tracks.pop(index)
        except IndexError:
            raise ValueError(f"Index {index} is out of bounds for playlist")

    def clear_playlist(self) -> None:
        """
        Method to clear all Track objects from the playlist.

        Arguments:
            None

        Returns:
            None

        Raises:
            
        """
        try:
            self._tracks.clear()
        except:
            raise ValueError("Could not clear the playlist.")

    # utility methods
    def __iter__(self):
        """Iterate over all tracks in self._tracks."""
        return iter(self._tracks)
