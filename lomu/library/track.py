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

        Returns:
            (AudioFormat): The associated, parsed AudioFormat.

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
        album_art (bytes | None): The byte data of the file's album art.
        audio_format (AudioFormat): The type of audio format the track is in.
    """
    file_path: Path
    title: str
    artist: str
    album: str
    release_date: str
    track_number: int
    duration: float
    album_art: Optional[bytes] = None
    audio_format: AudioFormat = field(init=False)

    def __post_init__(self):
        """
        A post-constructor to dynamically set some frozen dataclass attributes.
        """
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

    @staticmethod
    def _validate_date_parts(date: str) -> str:
        """
        Validates that date parts are within valid ranges
        If the month or day is an invalid number, both will default to 01.
        If the format is valid, the date itself is returned.

        Arguments:
            date (str): The date string to validate.

        Returns:
            (str): A string of the validated date.

        Raises:
            None
        """
        date_parts: list[str] = str(date).replace("/", "-").split("-")

        if len(date_parts) == 3:
            year, month, day = date_parts
            
            if not (1 <= int(month) <= 12) or not (1 <= int(day) <= 31):
                return f"{year}-01-01"
            else:
                return str(date)
        else:
            return str(date)

    @staticmethod
    def _normalize_date(date: str) -> str:
        """
        Ensures that a provided date string is of a valid format.
        Valid inputs: 'YYYY-MM-DD', 'YYYY', 'YY-MM-DD'

        Arguments:
            date (str): The date string to validate and normalize.

        Returns:
            (str): A string of the normalized date formatted to 'YYYY-MM-DD'.

        Raises:
            ValueError: If the inputted string is of no valid format.
        """
        date = Track._validate_date_parts(date)

        valid_formats: list[str] = ["%Y-%m-%d", "%y-%m-%d", "%Y"]

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
