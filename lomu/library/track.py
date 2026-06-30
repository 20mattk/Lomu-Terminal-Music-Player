from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from datetime import datetime


class AudioFormat(str, Enum):
    """
    Represents the only valid audio file formats the application can use.
    This Enum is used as a data type for an attribute in the Track class.
    """
    MP3 = ".mp3"
    FLAC = ".flac"
    WAV = ".wav"

    @classmethod
    def from_suffix(cls, suffix: str) -> AudioFormat:
        """
        Derives the audio format from the file type extension.
        Ensures the extension is of a valid audio format in the class.
        Hanldes the missing or present leading "." in a file type.

        Arguments:
            cls (AudioFormat): The AudioFormat class passed by @classmethod.
            suffix (str): The file type extension to parse through.

        Raises:
            ValueError: The file type extension isn't supported in AudioFormat.
        """
        suffix = suffix.lower()

        if not suffix:
            raise ValueError("file_path has no extension/suffix.")
        if not suffix.startswith("."):
            suffix = "." + suffix

        try:
            return cls(suffix)
        except ValueError:
            raise ValueError(
                f"{suffix} is an unsupported audio extension."
                f" Supported: {', '.join(format.value for format in cls)}"
            )


@dataclass(slots=True, frozen=True)
class Track:
    """
    Track simply represents a trakc's data.

    Instances are immuatable to prevent accidental modification and to enable
    use in playlists.

    Attributes:
        file_path (Path): Object pointing to the audio file.
        title (str): Title of the track.
        artist (str): The artist that the track belongs to.
        album (str): The album that the track belongs to.
        release_date (str): 'YYYY-MM-DD' date on which the album was released.
        track_number (int): The order in which the track appears on its album.
        duration (float): The length in seconds of the track.
    """
    file_path: Path
    title: str
    artist: str
    album: str
    release_date: str
    track_number: int
    duration: float
    audio_format: AudioFormat = field(init=False)

    def __post_init__(self):
        if self.track_number <= 0:
            raise ValueError("track_number must be greater than 0.")

        object.__setattr__(
            self,
            "release_date",
            self._normalize_date(self.release_date)
        )

        object.__setattr__(
            self,
            "audio_format",
            AudioFormat.from_suffix(self.file_path.suffix)
        )

    def _normalize_date(self, date: str) -> str:
        """
        Ensures that a provided date string is of a valid format.
        If the format is valid, the date is transformed into 'YYYY-MM-DD'.
        Valid inputs: 'YYYY-MM-DD', 'YYYY', 'YY-MM-DD'

        Arguments:
            self (Track): The instance of the Track class.
            date (str): The date string to validate and normalize.

        Returns:
            (str): A string of the valid date formatted to 'YYYY-MM-DD'.

        Raises:
            ValueError: If the inputted string is of no valid format.
        """
        valid_formats: list[str] = ["%Y-%m-%d", "%Y", "%y-%m-%d"]

        for valid_format in valid_formats:
            try:
                return datetime.strptime(
                    date, valid_format
                ).strftime("%Y-%m-%d")
            except:
                pass

        raise ValueError(
            f"Invalid date format: {date}. "
            f"Valid formats: {valid_formats}."
        )
