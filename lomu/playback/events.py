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


# enum EventType:
#     TRACK_STARTED
#     TRACK_PAUSED
#     TRACK_RESUMED
#     TRACK_STOPPED
#     TRACK_FINISHED
#     QUEUE_CHANGED
#     VOLUME_CHANGED
#     PLAYER_ERROR
#     PLAYER_CLOSED
#     etc.


# @dataclass(frozen=True)
# class PlaybackEvent:
#     type: EventType
#     track: Track | None
#     value: object | None
#     message: str | None


# class EventBus:
    # keeps track of the current queue
    # emits (puts) events