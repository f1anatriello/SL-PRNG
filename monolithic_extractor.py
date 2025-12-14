import hashlib # For hashing functions
import struct # For packing and unpacking binary data

''' This class implements a seedless pseudo-random number generator (PRNG) 
using a monolithic extractor approach. 
It maintains an internal state and generates pseudo-random bytes on demand. 
The state can be refreshed with additional entropy data. '''

class MonolithicPRNG:
    def __init__(self):
        '''Constructor to initialize the PRNG state'''
        self.state = b"\x00" * 32  # 256-bit state initialized to zero
        self.counter = 0  # Counter for generating unique outputs

    def refresh(self, data: bytes):
        '''Update the internal state like a monolithic extractor, hashing everything in one shot'''
        self.state = hashlib.sha256(self.state + data).digest()  # Update state using SHA-256 hash

    def next(self, n: int) -> bytes:
        '''Generate the next n bytes of pseudo-random data'''
        output = b""  # Initialize the buffer for output bytes
        while len(output) < n:
            counter_bytes = struct.pack("<Q", self.counter)  # Pack counter as 8-byte little-endian
            output += hashlib.sha256(self.state + counter_bytes).digest()  # Generate new bytes using SHA-256
            self.counter += 1  # Increment counter for next call
        return output[:n] 
    
