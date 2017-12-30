import numpy as np


class RingBuffer:
    # Ring buffer using numpy arrays
    def __init__(self, length):
        self.data = np.zeros([length, 2], dtype='f')
        self.index = 0

    def extend(self, x):
        # Adds array x to ring buffer
        x_index = (self.index + np.arange(x.shape[0])) % self.data.shape[0]
        self.data[x_index, :] = x
        self.index = x_index[-1] + 1

    def get(self):
        # Returns the first-in-first-out data in the ring buffer
        idx = (self.index + np.arange(self.data.shape[0])) % self.data.shape[0]
        return self.data[idx, :]


if __name__ == '__main__':
    r = RingBuffer(6)
    print(r.get())

