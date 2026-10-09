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