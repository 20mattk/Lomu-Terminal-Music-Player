from .track import Track, AudioFormat
from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE


UNKNOWN_TITLE: str = "Unknown Title"
UNKNOWN_ARTIST: str = "Unknown Artist"
UNKNOWN_ALBUM: str = "Unknown Album"
UNKNOWN_RELEASE_DATE: str = "0001"
UNKNOWN_TRACK_NUMBER: str = "1"


def _first_str(values: Iterable[object] | None) -> str:
    """Return first non-blank value of an iterable as stripped string or ""."""
    for value in values or ():
        text: str = str(value).strip()
        if text:
            return text
    return ""


def _format_date(raw_str: str) -> str:
    """Truncate a time of day from a date and time string. (YYYY-MM-DD)"""
    return raw_str.split("T", 1)[0]


def _format_track_number(raw_str: str) -> int:
    """
    Parse various track number reads as a single integer.
    '7', '07', '7/12' become 7.
    Garbage numbers default to 1.
    """
    try:
        track_number: int = int(raw_str.split("/")[0])
    except ValueError:
        return 1
    return track_number if track_number > 0 else 1

def _get_album_art(pictures: Iterable) -> bytes | None:
    """Return the album art bytes, the first image, or None."""
    first: bytes | None = None
    for picture in pictures:
        if picture.type == 3:
            return picture.data
        if first is None:
            first = picture.data
    return first


class MetadataExtractor(ABC):
    """
    Abstract class defining an interface to be implemented.
    Can not be instantiated from, only inhereted from.

    Child classes must implement the abstract method defined here.
    """
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Track:
        pass

    @abstractmethod
    def _tag_as_str(self, tags, default: str, *keys: str) -> str:
        pass


class MP3MetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .mp3 file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        """
        The inherited abstract method which has been defined for .mp3 files.
        Creates and returns a Track object.

        Arguments:
            file_path (Path): The file path to the .mp3 file.

        Returns:
            (Track): The Track object created from the .mp3 file.

        Raises:
            None
        """
        audio: MP3 = MP3(file_path)
        tags: ID3 | None = audio.tags

        return Track(
            file_path=file_path,
            title=self._tag_as_str(tags, UNKNOWN_TITLE, "TIT2"),
            artist=self._tag_as_str(tags, UNKNOWN_ARTIST, "TPE1"),
            album=self._tag_as_str(tags, UNKNOWN_ALBUM, "TALB"),
            release_date=_format_date(
                self._tag_as_str(tags, UNKNOWN_RELEASE_DATE, "TDRC", "TDOR")
            ),
            track_number=_format_track_number(
                self._tag_as_str(tags, UNKNOWN_TRACK_NUMBER, "TRCK")
            ),
            duration=audio.info.length,
            album_art=_get_album_art(
                tags.getall("APIC") if tags is not None else ()
            )
        )

    def _tag_as_str(self, tags: ID3 | None, default: str, *keys: str) -> str:
        """
        Helper function to ensure track metadata is parsed as a string.
        
        Arguments:
            tags (ID3 | None): The audio metadata.
            keys (str): The pieces of metadata to parse in order.
            default (str): The default value to use if the key doesn't work.
        
        Returns:
            (str): The string representation of the extracted piece of metadata.
        
        Raises:
            None
        """
        if tags is not None:
            for key in keys:
                frame = tags.get(key)
                text: str = _first_str(frame.text) if frame is not None else ""
                if text:
                    return text
        return default


class FLACMetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .flac file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        """
        The inherited abstract method which has been defined for .flac files.
        Creates and returns a Track object.

        Arguments:
            file_path (Path): The file path to the .flac file.

        Returns:
            (Track): The Track object created from the .flac file.

        Raises:
            None
        """
        audio: FLAC = FLAC(file_path)
        tags = audio.tags

        album_art: bytes | None = (
            audio.pictures[0].data if audio.pictures else None
        )

        return Track(
            file_path=file_path,
            title=self._tag_as_str(tags, UNKNOWN_TITLE, "title"),
            artist=self._tag_as_str(tags, UNKNOWN_ARTIST, "artist"),
            album=self._tag_as_str(tags, UNKNOWN_ALBUM, "album"),
            release_date=_format_date(
                self._tag_as_str(tags, UNKNOWN_RELEASE_DATE, "date")
            ),
            track_number=_format_track_number(
                self._tag_as_str(tags, UNKNOWN_TRACK_NUMBER, "number")
            ),
            duration=audio.info.length,
            album_art=_get_album_art(audio.pictures)
        )

    def _tag_as_str(self, tags, default: str, *keys: str) -> str:
        """
        Helper function to ensure track metadata is parsed as a string.
        
        Arguments:
            tags (Mapping[str, list[str]] | None): The audio metadata.
            default (str): The default value to use if the key doesn't work.
            keys (str): The pieces of metadata to parse in order.
        
        Returns:
            (str): The string representation of the extracted piece of metadata.
        
        Raises:
            None
        """
        if tags is not None:
            for key in keys:
                text: str = _first_str(tags.get(key))
                if text:
                    return text
        return default


class WAVMetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .wav file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        """
        The inherited abstract method which has been defined for .wav files.
        Creates and returns a Track object.

        Arguments:
            file_path (Path): The file path to the .wav file.

        Returns:
            (Track): The Track object created from the .wav file.

        Raises:
            None
        """
        audio: WAVE = WAVE(file_path)
        tags: ID3 | None = audio.tags

        return Track(
            file_path=file_path,
            title=self._tag_as_str(tags, UNKNOWN_TITLE, "TIT2"),
            artist=self._tag_as_str(tags, UNKNOWN_ARTIST, "TPE1"),
            album=self._tag_as_str(tags, UNKNOWN_ALBUM, "TALB"),
            release_date=_format_date(
                self._tag_as_str(tags, UNKNOWN_RELEASE_DATE, "TDRC", "TDOR")
            ),
            track_number=_format_track_number(
                self._tag_as_str(tags, UNKNOWN_TRACK_NUMBER, "TRCK")
            ),
            duration=audio.info.length,
            album_art=_get_album_art(
                tags.getall("APIC") if tags is not None else ()
            )
        )

    def _tag_as_str(self, tags: ID3 | None, default: str, *keys: str) -> str:
        """
        Helper function to ensure track metadata is parsed as a string.
        
        Arguments:
            tags (ID3 | None): The audio metadata.
            keys (str): The pieces of metadata to parse in order.
            default (str): The default value to use if the key doesn't work.
        
        Returns:
            (str): The string representation of the extracted piece of metadata.
        
        Raises:
            None
        """
        if tags is not None:
            for key in keys:
                frame = tags.get(key)
                text: str = _first_str(frame.text) if frame is not None else ""
                if text:
                    return text
        return default


class MetadataFactory:
    """
    Creator of the Factory Method.
    Ingests a file type extension, returns the corresponding implementation.

    Uses a factory method to determine which implementation to return.
    """
    def create_extractor(self, audio_format: AudioFormat) -> MetadataExtractor:
        """
        Factory Method which returns the concrete implementation.
        Given a file extension, return an object of the corresponding type.

        Arguments:
            audio_format (AudioFormat): The file audio type to create for.

        Returns:
            (MetadataExtractor): The concrete implementation extractor desired.

        Raises:
            (ValueError): If the desired file type is unsupported.
        """
        if audio_format == AudioFormat.MP3:
            return MP3MetadataExtractor()
        if audio_format == AudioFormat.FLAC:
            return FLACMetadataExtractor()
        if audio_format == AudioFormat.WAV:
            return WAVMetadataExtractor()
        else:
            raise ValueError(f"Unsupported file type: {audio_format}")


def load_track(file_path: Path | str) -> Track:
    """
    The function to expose to the rest of the application.
    This acts as the access point to the Factory Method.

    Arguments:
        file_path (Path): Path to the audio file to extract data from.

    Returns:
        (Track): The file's extracted metadata as a Track object.

    Raises:
        (FileNotFoundError): If the passed file cannot be found.
    """
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    audio_format: AudioFormat = AudioFormat.from_suffix(file_path.suffix)

    factory: MetadataFactory = MetadataFactory()
    extractor: MetadataExtractor = factory.create_extractor(audio_format)

    return extractor.extract_metadata(file_path)
