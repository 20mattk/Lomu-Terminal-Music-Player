# TODO
# I will re-structure the playback module according to the below:
# lomu/
# └── playback/
#     ├── __init__.py
#     ├── queue.py       # Track scope/eligibility for current playback session
#     ├── sequence.py    # Ordering and shuffling of Tracks in the Queue
#     ├── controller.py  # Track playback state (play/next, etc, send to Player)
#     ├── player.py      # Audio playback with VLC and event reporting
#     └── events.py      # Defines events to be reported by the Player