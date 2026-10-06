from ..library import Library, Track


class PlaybackQueue:
    def __init__(self):
        # copy tracks into internal track list
        # if internal track list is not empty: set curr idx to 0
        # else: set curr idx to nothing
        # tracks
        # current index
        # lock
        # repeat mode
        # shuffle mode
        pass
    
    # immutable properties
    @property
    def tracks(self) -> list[Track] | list[None]:
        """Return a copy of the internal Track object list."""
        # acquire lock
        # return internal tracks list
        # release lock
        pass
    
    @property
    def current_track(self) -> Track | None:
        """Return the Track object at the current index."""
        # acquire lock
        # return internal current track
        # release lock
        pass
    
    # utility methods
    def add(self, track: Track) -> None:
        """Add a Track object to the playback queue."""
        # acquire lock
        # append track
        # release lock
        pass

    def clear(self) -> None:
        """Clear all Track objects from the playback queue."""
        # acquire lock
        # clear tracks
        # current index = None
        # release lock
        pass

    def next(self) -> None:
        """Skip to the next Track object in the playback queue."""
        # acquire lock
        # if queue is empty: return None
        # if repeat_mode is ONE: return current track

        # if current_index is None: current_index = 0
        # elif another track exists: current_index += 1
        # elif repeat_mode is ALL: current_index = 0
        # else: current_index = None, return None
        # return tracks[current_index]
        # release lock
        pass

    def previous(self) -> None:
        """Return to the previous Track object in the playback queue."""
        # acquire lock
        # calculate previous index
        # return selected track
        # release lock
        pass