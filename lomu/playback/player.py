import vlc
from enum import Enum, auto
from ..library import Track


class PlayerState(Enum):
    """Represents the valid states of the player. Synchronized with VLC."""
    IDLE = auto()       # vlc.State.NothingSpecial = 0
    OPENING = auto()    # vlc.State.Opening = 1
    BUFFERING = auto()  # vlc.State.Buffering = 2
    PLAYING = auto()    # vlc.State.Playing = 3
    PAUSED = auto()     # vlc.State.Paused = 4
    STOPPED = auto()    # vlc.State.Stopped = 5
    ENDED = auto()      # vlc.State.Ended = 6
    ERROR = auto()      # vlc.State.Error = 7


class Player():
    """
    The class for controlling the playback of an individual Track object.
    Built on top of Python's VLC library.
    """
    def __init__(self) -> None:
        instance = vlc.Instance("--no-video")
        if instance is None:
            raise RuntimeError("Could not initialize VLC.")

        self._vlc_instance: vlc.Instance = instance
        self._player: vlc.MediaPlayer = self._vlc_instance.media_player_new()
        self._current_media: vlc.Media | None = None

        self._player_state: PlayerState = PlayerState.IDLE
        self._current_track: Track | None = None
        # self._events: EventBus  # to be implemented later

    # === properties === #
    @property
    def state(self) -> PlayerState:
        return self._player_state

    @property
    def is_playing(self) -> bool:
        return self._player_state == PlayerState.PLAYING

    @property
    def is_paused(self) -> bool:
        return self._player_state == PlayerState.PAUSED

    @property
    def current_track(self) -> Track | None:
        return self._current_track

    @property
    def volume(self) -> int:
        return self._player.audio_get_volume()

    @property
    def position(self) -> int:
        return self._player.get_time()

    @property
    def duration(self) -> int:
        return self._player.get_length()

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