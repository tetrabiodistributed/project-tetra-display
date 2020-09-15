import unittest

from ringbuffer import RingBuffer


class TestRingBuffer(unittest.TestCase):

    def test_fills(self):
        r = RingBuffer(10)
        for i in range(10):
            r.append(i)
        self.assertEqual(r, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                         "Fails to fill buffer.")

    def test_wraps(self):
        r = RingBuffer(10)
        for i in range(20):
            r.append(i)
        self.assertEqual(r, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                         "Fails to wrap buffer when more data is added "
                         "than the max buffer length.")

    def test_raises_error_on_index_empty_buffer(self):
        r = RingBuffer(10)
        with self.assertRaises(IndexError,
                               msg="Fails to raise error when an empty "
                               "buffer gets indexed."):
            r[0]

    def test_partly_filled_buffer(self):
        r = RingBuffer(10)
        for i in range(5):
            r.append(i)
        self.assertEqual(r, [0, 1, 2, 3, 4],
                         "Fails to partly fill a buffer.")

    def test_negative_index_on_partly_filled_buffer(self):
        r = RingBuffer(10)
        for i in range(5):
            r.append(i)
        self.assertEqual(r[-1], 4,
                         "Fails to return the most recent datum when "
                         "asked for index -1.")

    def test_two_similar_ringbuffers_are_equal(self):
        r = RingBuffer(10)
        s = RingBuffer(10)
        for i in range(20):
            r.append(i)
            s.append(i)
        self.assertEqual(r, s,
                         "Fails to say that two identically filled "
                         "RingBuffers are equal.")

    def test_string_shows_buffer_and_length(self):
        r = RingBuffer(10)
        for i in range(20):
            r.append(i)
        self.assertEqual(str(r), "<RingBuffer of length 10 and "
                                 "[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]>",
                         "Fails to print RingBuffer to spec.")

    def test_can_define_initial_state(self):
        r = RingBuffer(10, initial_state=[5]*10)
        self.assertEqual(r, [5]*10,
                         "Fails to initialize a RingBuffer to a "
                         "particular state.")
