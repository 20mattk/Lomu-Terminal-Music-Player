# === TODO === #
# 1. Finish MP3 tag extraction
# 2. Finish WAV tag extraction
# 3. Implement album_art image (path or data) extraction


from .track import Track, AudioFormat
from abc import ABC, abstractmethod
from pathlib import Path
from mutagen.id3 import ID3
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
        audio: ID3 = ID3(file_path)

        title: str = audio.get("TIT2", "Unknown Title")
        artist: str = audio.get("TPE1", "Unknown Artist")
        album: str = audio.get("TALB", "Unknown Album")
        release_date: str = audio.get("TDRL", "Unknown Release Date")
        track_number: int = int(
            audio.get("TRCK", "Unknown Track Number").text[0]
        )
        duration: float = File(file_path).info.length
        # album_art

        print(
            f"File Path: {file_path}\n"
            f"Title: {title}\n"
            f"Artist: {artist}\n"
            f"Album: {album}\n"
            f"Release Date: {release_date}\n"
            f"Track Number: {track_number}\n"
            f"Duration: {duration}\n"
            # f"Album Art: {album_art}\n"
        )

        # return Track(
        #     file_path=file_path,
        #     title="Title",
        #     artist="Artist",
        #     album="Album",
        #     release_date="1907-01-01",
        #     track_number=1,
        #     duration=180.00
        #     album_art=album_art
        # )

        pass


class FLACMetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .flac file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        audio: FLAC = FLAC(file_path)

        title: str = audio.get("title", ["Unknown Title"])[0]
        artist: str = audio.get("artist", ["Unknown Artist"])[0]
        album: str = audio.get("album", ["Unknown Album"])[0]
        release_date: str = audio.get("date", ["Unknown Release Date"])[0]
        track_number: int = int(
            audio.get("number", ["Unknown Track Number"])[0]
        )
        duration: float = File(file_path).info.length
        # album_art

        return Track(
            file_path=file_path,
            title=title,
            artist=artist,
            album=album,
            release_date=release_date,
            track_number=track_number,
            duration=duration
            # album_art=album_art
        )


class WAVMetadataExtractor(MetadataExtractor):
    """
    Concrete implementation of the MetadataExtractor interface.
    Extracts .wav file metadata to generate a Track object.
    """
    def extract_metadata(self, file_path: Path) -> Track:
        # print(WAVE(file_path))
        audio: WAVE = WAVE(file_path)

        # title = "TIT2"
        # artist = "TPE1"
        # album = "TALB"
        # release_date = "
        # track_number = "TRCK"
        # duration = 
        # ? album_art = "APIC" ?

        title: str = audio.get("TIT2", ["Unknown Title"])[0]
        artist: str = audio.get("TPE1", ["Unknown Artist"])[0]
        album: str = audio.get("TALB", ["Unknown Album"])[0]
        release_date: str = audio.get("date", ["Unknown Release Date"])[0]
        track_number: str = int(audio.get("TRCK", ["Unknown Track Number"])[0].split("/")[0])
        duration: float = File(file_path).info.length
        # album_art

        print(
            f"File Path: {file_path}\n"
            f"Title: {title}\n"
            f"Artist: {artist}\n"
            f"Album: {album}\n"
            f"Release Date: {release_date}\n"
            f"Track Number: {track_number}\n"
            f"Duration: {duration}\n"
            # album_art
        )

        # return Track(
        #     file_path=file_path,
        #     title="Title",
        #     artist="Artist",
        #     album="Album",
        #     release_date="1907-01-01",
        #     track_number=1,
        #     duration=180.00
        #     album_art
        # )

        pass


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
