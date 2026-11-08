import vlc
from enum import Enum, auto
from ..library import Track


class PlayerState(Enum):
    """Represents the valid states of the player."""
    IDLE = auto()
    LOADING = auto()
    PLAYING = auto()
    PAUSED = auto()
    STOPPED = auto()
    ERROR = auto()


class Player():
    """<Docstring>."""
    def __init__(self) -> None:
        # _vlc_instance: vlc.Instance       # creates/manages VLC media rsrcs
        # _media_player: vlc.MediaPlayer    # controls actual audio playback
        # _current_media: vlc.Media | None  # holds current VLC media object

        # _player_state: PlayerState        # the app's playback state
        # _current_track: Track             # currently-loaded track
        # _volume: int                      # current VLC volume setting
        # _events: ?EventBus?               # publishes playback events
        pass

    # properties
    # state          # internal attribute
    # current_track  # internal attribute
    # volume         # vlc audio_get_volume()
    # is_playing     # vlc is_playing()
    # is_paused      # vlc get_state()
    # posiiton       # vlc get_time()
    # duration       # vlc get_length()

    # public methods
    def load(self, track: Track) -> None:
        # vlc: set_media()
        pass

    def play(self) -> None:
        # vlc: play()
        pass

    def pause(self) -> None:
        # vlc: set_pause(1)
        pass

    def resume(self) -> None:
        # vlc: set_pause(0)
        pass

    def stop(self) -> None:
        # vlc: stop()
        pass

    def seek(self, position: float) -> None:
        # vlc: set_time()
        pass

    def set_volume(self, volume: int) -> None:
        # vlc: audio_set_volume()
        pass

    def close(self) -> None:
        # vlc: release()
        pass

    # private methods
    def _set_state(self) -> None:
        # update internal player state
        raise NotImplementedError

    def _validate_track(self, track: Track) -> bool:
        # validate track instance
        raise NotImplementedError

    def _validate_volume(self, volume: int) -> bool:
        # validate between 0 - 100
        raise NotImplementedError

    # _validate_position(): validate seek position
    # _publish_event(): publish through ?EventBus?
    # _attach_events(): register vlc event listeners?
    # _handle_vlc_events(): hanlde events from vlc