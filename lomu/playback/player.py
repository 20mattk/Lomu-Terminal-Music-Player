import vlc
import threading
from pathlib import Path
from ..library import Library, Track


class Player:
    def __init__(self) -> None:
        # vlc components
        self._vlc_instance = vlc.Instance()
        self._media_list_player = self._vlc_instance.media_list_player_new()
        self._media_list = self._vlc_instance.media_list_new()

        # state management
        self._is_playing: bool = False
        self._current_track: Track = None
        self._playback_thread: threading.Thread = None

    # properties
    def is_playing(self) -> bool:
        """Returns the status of _is_playing."""
        return self._is_playing

    # playback methods
    def start(self, track: Track) -> None:
        """
        Starts a playback thread for the supplied Track object.
        Will do nothing if a Track object is currently in playback.
        """
        if self._is_playing:
            print(
                "Playback In Progress: "
                f"{self._current_track.artist} - {self._current_track.title}"
            )
            return

        self._is_playing = True
        self._current_track = track
        
        print(
            "Playback Started: "
            f"{self._current_track.artist} - {self._current_track.title}"
        )

        self._playback_thread = threading.Thread(
            target=self._play_loop,
            args=(track,)
        )
        self._playback_thread.start()

    def pause(self) -> None:
        """Pauses the playback of the current Track object."""
        if self._is_playing and self._media_list_player.is_playing():
            self._media_list_player.pause()
            print(
                "Playback Paused: "
                f"{self._current_track.artist} - {self._current_track.title}"
            )

    def stop(self) -> None:
        """Stops playback of the VLC media and rejoins the playback thread."""
        if self._is_playing:
            self._media_list_player.stop()

        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join()

        print("Playback Stopped")

        self._is_playing = False
        self._current_track = None

    def skip(self) -> None:
        pass

    def rewind(self) -> None:
        pass

    def seek(self) -> None:
        pass

    # utility methods
    def _play_loop(self, track: Track) -> None:
        """
        Handles the actual beginning of playback for the Track object.
        Adds the track to _media_list and plays it with _media_list_player.

        Arguments:
            track (Track): The Track to begin playback for.

        Returns:
            None

        Raises:
            (Exception): If playback cannot be started.
        """
        try:
            self._media_list.add_media(
                self._vlc_instance.media_new(track.file_path)
            )
            self._media_list_player.set_media_list(self._media_list)

            self._media_list_player.play()

        except Exception as e:
            print(f"Playback Error: {e}")
            self.stop()
