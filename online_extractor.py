import hashlib # For hashing functions
import struct # For packing and unpacking binary data

''' This class implements a seedless pseudo-random number generator (PRNG) 
using an online extractor approach. 
It maintains an internal state and generates pseudo-random bytes on demand. 
The state can be refreshed with additional entropy data. '''

class OnlinePRNG:
    def __init__(self):
        '''Constructor to initialize the PRNG state'''
        self.state = b"\x00" * 32  # 256-bit state initialized to zero
        self.counter = 0  # Counter for generating unique outputs

    def refresh(self, data: bytes):
        '''Update the internal state like an online extractor, absorbing data gradually'''
        h = hashlib.blake2s(digest_size=32)
        h.update(self.state)
        h.update(data)
        self.state = h.digest()

    def next(self, n: int) -> bytes:
        '''Generate the next n bytes of pseudo-random data'''
        output = b""  # Initialize the buffer for output bytes
        while len(output) < n:
            counter_bytes = struct.pack("<Q", self.counter)  # Pack counter as 8-byte little-endian
            h = hashlib.blake2s(key=self.state, digest_size=32)
            h.update(counter_bytes) 
            output += h.digest()
            self.counter += 1
        return output[:n]
