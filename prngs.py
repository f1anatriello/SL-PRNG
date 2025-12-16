class SeedlessLCG:
    def __init__(self, seed=0, a:int=1664525, c:int=1013904223, m:int=2**32):
        self.state = seed # Current state of the LCG - starting with 0, because of missing seed
        self.a = a # Multiplier
        self.c = c # Increment
        self.m = m # Modulus

    def refresh(self, data: bytes):
        '''Refresh the state with additional entropy data'''
        entropy = int.from_bytes(data, 'big')
        self.state = (self.state + entropy) % self.m

    def next(self, n: int) -> bytes:
        '''Generate the next pseudo-random number'''
        output = bytearray()
        for _ in range(n):
            self.state = (self.a * self.state + self.c) % self.m # LCG formula
            output.append((self.state >> 16) & 0xFF) # Extract one byte from the state
        return bytes(output) 
    

class SeedlessRC4:
    def __init__(self):
        self.S = list(range(256))
        self.i = 0
        self.j = 0
        self.key_set = False

    def refresh(self, data: bytes):
        key = list(data)
        key_len = len(key)
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % key_len]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0
        self.key_set = True

    def next(self, n: int):
        if not self.key_set:
            raise ValueError("Key must be set via refresh() before generating output")

        output = bytearray()
        for _ in range(n):
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.S[self.i]) % 256
            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
            t = (self.S[self.i] + self.S[self.j]) % 256
            output.append(self.S[t])
        return bytes(output)


class SeedlessXorshift:
    def __init__(self):
        self.state = 2463534242  # default seed

    def refresh(self, data: bytes):
        self.state = int.from_bytes(data, 'big') or 1

    def next(self, n: int):
        output = bytearray()
        for _ in range(n):
            self.state ^= (self.state << 13) & 0xFFFFFFFF
            self.state ^= (self.state >> 17)
            self.state ^= (self.state << 5) & 0xFFFFFFFF
            output.append(self.state & 0xFF)
        return bytes(output)
