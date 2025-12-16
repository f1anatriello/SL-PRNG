import hashlib
import hmac
import struct



class MonolithicPRNG:
    ''' This class implements a seedless pseudo-random number generator (PRNG) 
    using a monolithic extractor approach. 
    It maintains an internal state and generates pseudo-random bytes on demand. 
    The state can be refreshed with additional entropy data. '''
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
    


class OnlinePRNG:
    ''' This class implements a seedless pseudo-random number generator (PRNG) 
    using an online extractor approach. 
    It maintains an internal state and generates pseudo-random bytes on demand. 
    The state can be refreshed with additional entropy data. '''

    
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


class HKDFStylePRNG:
    ''' This class implements a seedless pseudo-random number generator (PRNG) 
    using a HKDF-style extractor (extract-then-expand) approach. 
    It maintains an internal state and generates pseudo-random bytes on demand. 
    The state can be refreshed with additional entropy data. '''

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