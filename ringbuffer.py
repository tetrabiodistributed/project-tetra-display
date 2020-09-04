import collections


class RingBuffer(collections.deque):

    def __init__(self, max_length):
        self._max_length = max_length
        super().__init__(maxlen=max_length)

    def __eq__(self, other):
        return list(self) == list(other)

    def __str__(self):
        return (f"<RingBuffer of length {self._max_length} and "
                f"{list(self)}>")
