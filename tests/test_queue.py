"""
Possible Tests

- Creating an empty queue and a pre-populated queue.
- Adding one track and multiple tracks.
- Adding the same track multiple times.
- Checking `len(queue)` after mutations.
- Iterating over tracks in the expected order.
- Verifying the `tracks` snapshot cannot mutate the internal list.
- Removing the first, middle, and last entries by index.
- Handling invalid indices and empty queues.
- Clearing the queue.
- Moving tracks between positions.
- Shuffling preserves all entries without requiring a particular random order.
- Peeking leaves the queue unchanged.
- Popping returns the first track and removes exactly one entry.
"""