# === TODO =================================================================== #

# I will re-structure the playback module according to the below:
# lomu/
# └── playback/
#     ├── __init__.py
#     ├── context.py     # Track scope/eligibility for current playback session
#     ├── queue.py       # Ordering and shuffling of Tracks in the Queue
#     ├── controller.py  # Track playback state (play/next, etc, send to Player)
#     ├── player.py      # Audio playback with VLC and event reporting
#     └── events.py      # Defines events to be reported by the Player

# Development Order:
# 1. context.py
# 2. queue.py
# 3. events.py
# 4. player.py
# 5. controller.py

# ============================================================================ #


from ..library import Track
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class PlaybackContext:
    """A data contianer for the scope of Tracks to be given to the queue."""

    tracks: tuple[Track, ...]
    source: str | None = None

    @classmethod
    def from_tracks(
        cls, tracks: Iterable[Track], source: str | None = None
    ) -> PlaybackContext:
        """Create a context of Tracks from an iterable of Tracks."""
        return cls(tracks=tuple(tracks), source=source)