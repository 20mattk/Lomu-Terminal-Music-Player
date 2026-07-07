from .track import Track, AudioFormat
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen import File


class MetadataExtractor(ABC):
    """
    Abstract class defining an interface to be implemented.
    Can not be instantiated from, only inhereted from.

    Child classes must implement the abstract method defined here.
    """
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Track:
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
        """
        audio: ID3 = ID3(file_path)

        title: str = audio.get("TIT2", "Unknown Title")
        artist: str = audio.get("TPE1", "Unknown Artist")
        album: str = audio.get("TALB", "Unknown Album")
        release_date: str = str(
            audio.get("TDOR", str(audio.get("TDRC", "0001")))
        )
        track_number: int = int(audio.get("TRCK", "1").text[0].split("/")[0])
        duration: float = File(file_path).info.length
        album_art: Optional[bytes] = None
        for frame in audio.values():
            if isinstance(frame, APIC):
                album_art = frame.data
                break

        return Track(
            file_path=file_path,
            title=title,
            artist=artist,
            album=album,
            release_date=release_date,
            track_number=track_number,
            duration=duration,
            album_art=album_art
        )


class FLACMetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .flac file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        """
        The inherited abstract method which has been defined for .flac files.
        Creates and returns a Track object.
        """
        audio: FLAC = FLAC(file_path)

        title: str = audio.get("title", ["Unknown Title"])[0]
        artist: str = audio.get("artist", ["Unknown Artist"])[0]
        album: str = audio.get("album", ["Unknown Album"])[0]
        release_date: str = audio.get("date", ["0001"])[0]
        track_number: int = int(audio.get("number", ["1"])[0])
        duration: float = File(file_path).info.length
        album_art: Optional[bytes] = (
            audio.pictures[0].data if audio.pictures else None
        )

        return Track(
            file_path=file_path,
            title=title,
            artist=artist,
            album=album,
            release_date=release_date,
            track_number=track_number,
            duration=duration,
            album_art=album_art
        )


class WAVMetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .wav file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        """
        The inherited abstract method which has been defined for .wav files.
        Creates and returns a Track object.
        """
        audio: WAVE = WAVE(file_path)

        title: str = audio.get("TIT2", ["Unknown Title"])[0]
        artist: str = audio.get("TPE1", ["Unknown Artist"])[0]
        album: str = audio.get("TALB", ["Unknown Album"])[0]
        release_date: str = audio.get("TDRC", ["0001"])[0]
        track_number: str = int(audio.get("TRCK", ["1"])[0].split("/")[0])
        duration: float = File(file_path).info.length
        for frame in audio.values():
            if isinstance(frame, APIC):
                album_art = frame.data
                break

        return Track(
            file_path=file_path,
            title=title,
            artist=artist,
            album=album,
            release_date=release_date,
            track_number=track_number,
            duration=duration,
            album_art=album_art
        )


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
        """
        if audio_format == AudioFormat.MP3:
            return MP3MetadataExtractor()
        if audio_format == AudioFormat.FLAC:
            return FLACMetadataExtractor()
        if audio_format == AudioFormat.WAV:
            return WAVMetadataExtractor()
        else:
            raise ValueError(f"Unsupported file type: {extension}")


def load_track(file_path: str | Path) -> Track:
    file_path: Path = Path(file_path)
    audio_format: AudioFormat = AudioFormat(file_path.suffix.lower())

    factory: MetadataFactory = MetadataFactory()
    extractor: MetadataExtractor = factory.create_extractor(audio_format)

    return extractor.extract_metadata(file_path)
