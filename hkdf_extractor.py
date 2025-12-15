import hashlib
import hmac
import struct

''' This class implements a seedless pseudo-random number generator (PRNG) 
using a HKDF-style extractor (extract-then-expand) approach. 
It maintains an internal state and generates pseudo-random bytes on demand. 
The state can be refreshed with additional entropy data. '''

class HKDFStylePRNG:
    def __init__(self):
        '''Constructor to initialize the PRNG state'''
        self.state = b"\x00" * 32 # 256-bit state initialized to zero
        self.counter = 0 # Counter for generating unique outputs

    def refresh(self, data: bytes):
        '''Extract phase: update state using HMAC as extractor'''
        self.state = hmac.new(self.state, data, hashlib.sha256).digest()

    def next(self, n: int) -> bytes:
        '''Expand phase: generate output using HMAC-PRF on counter'''
        output = b""
        while len(output) < n:
            counter_bytes = struct.pack("<Q", self.counter)
            block = hmac.new(self.state, counter_bytes, hashlib.sha256).digest()
            output += block
            self.counter += 1
        return output[:n]