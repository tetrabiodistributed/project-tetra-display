import collections


class RingBuffer(collections.deque):
    """A ring buffer class based on collections.deque."""

    def __init__(self, max_length):
        """Initializes self.

        Parameters
        ----------
        max_length : int
            The length of the ring buffer.  If more elements are added
            than this, then the oldest elements will be overwritten.
        """
        self._max_length = max_length
        super().__init__(maxlen=max_length)

    def __eq__(self, other):
        """Returns self == other.  It supports other being a list,
        RingBuffer, or collections.deque.
        """
        return list(self) == list(other)

    def __str__(self):
        """Returns a string of the form
        <RingBuffer of length `max_length` and `list`>
        """
        return (f"<RingBuffer of length {self._max_length} and "
                f"{list(self)}>")
