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