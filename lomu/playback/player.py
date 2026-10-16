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


import vlc


# enum PlayerCommandType:
#     PLAY
#     PAUSE
#     RESUME
#     STOP
#     NEXT
#     PREVIOUS
#     SET_VOLUME
#     SHUTDOWN
#     etc.


# @dataclass(frozen=True)
# class PlayerCommand:
#     type: PlayerCommandType
#     value: object | None = None


# class Player:
# constructor(queue, backend):
#     initialize all state
#     create stop_event
#     create daemon=False worker thread
#     start worker thread
#     queue: PlaybackQueue
#     backend: AudioBackend
#     events: EventBus
#     commands: Queue[PlayerCommand]
#     worker: Thread
#     stop_event: Event
#     state_lock: Lock
#     player_state: PlayerState
#     volume: float
    # method play():
    #     commands.put(PlayerCommand(PLAY))

    # method pause():
    #     commands.put(PlayerCommand(PAUSE))

    # method resume():
    #     commands.put(PlayerCommand(RESUME))

    # method next():
    #     commands.put(PlayerCommand(NEXT))

    # method previous():
    #     commands.put(PlayerCommand(PREVIOUS))

    # method set_volume(value):
    #     validate value
    #     commands.put(PlayerCommand(SET_VOLUME, value))

    # method close():
    #     commands.put(PlayerCommand(SHUTDOWN))
    #     worker.join()
