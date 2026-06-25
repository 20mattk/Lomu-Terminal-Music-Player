from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum


class AudioFormat(str, Enum):
    """
    Represents the only valid audio file formats the application can use.

    This Enum is used as a data type for an attribute in the Track class.
    """
    MP3 = ".mp3"
    WAV = ".wav"
    FLAC = ".flac"

    @classmethod
    def from_suffix(cls, suffix: str) -> AudioFormat:
        """
        Derives the audio format from the file type extension.
        Ensures the extension is of a valid audio format in the class.
        Hanldes the missing or present leading . in a file type.

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
    Represents a music track with metadata.

    Instances are immuatable to prevent accidental modification and to enable
    use in playlists.

    Attributes:
        file_path (Path): Object pointing to the audio file.
        title (str): Title of the track.
        artist (str): The artist that the track belongs to.
        album (str): The album that the track belongs to.
        year (str): The year in which the track was released.
        track_number (int): The order in which the track appears on its album.
        duration (float): The length in seconds of the track.
    """
    file_path: Path
    title: str
    artist: str
    album: str
    year: str
    track_number: int
    duration: float
    audio_format: AudioFormat = field(init=False)

    def __post_init__(self):
        if self.track_number <= 0:
            raise ValueError("track_number must be greater than 0.")

        object.__setattr__(
            self,
            "audio_format",
            AudioFormat.from_suffix(self.file_path.suffix)
        )
