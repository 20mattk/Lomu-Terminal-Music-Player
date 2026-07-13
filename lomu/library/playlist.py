# will be mutable
# store collection of track objects
# need metadata about the playlist itself
# a unique identifier for the playlist


from .track import Track, AudioFormat
from uuid import UUID, uuid4


class Playlist:
    def __init__(self, name: str, description: str = "") -> None:
        self._id: UUID = uuid4()
        self._name: str = name
        self._description: str = description
        self._tracks: list[Track] = []

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
    # add_track(track: Track) -> None
    # remove_track(track: Track) -> None
    # remove_at(index: int) -> None
    # clear_playlist(track: Track) -> None
    # get_track_count() -> int
    # get_total_duration() -> float

    # utility methods
    def __iter__(self):
        """Iterate over all tracks in self._tracks."""
        return iter(self._tracks)
