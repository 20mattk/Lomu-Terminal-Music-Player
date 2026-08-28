import vlc
from ..library import Library, Track
from pathlib import Path


# tells vlc what to play and how to control it

# playback control
#   > play()
#   > pause()
#   > stop()
#   > skip()
#   > rewind()
#   > seek(time)

# state management
#   > is_playing
#   > current_track


class Player:
    def __init__(self, home_dir: Path) -> None:
        self.library: Library = Library(home_dir)
        self.is_playing: bool = False
        self.current_track: Track = None

    def __post_init__(self) -> None:  # this isn't being called for some reason
        try:
            self.library.populate_library()
            print(self.library.track_count)
        except Exception as e:
            print(e)


home_dir: Path = Path(input(" > File Path: "))

print(home_dir)

player: Player = Player(home_dir)
