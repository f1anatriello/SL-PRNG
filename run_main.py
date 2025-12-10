import time
import os
from seedless_prng import SeedlessPRNG

def main():
    rng = SeedlessPRNG()

    print("Start state:", rng.state.hex())

    out1 = rng.next(16)
    print("Output w/no entropy, just next:", out1.hex(), "\n")

    # Raccogli un po’ di entropia semplice e fai refresh
    entropy = time.time_ns().to_bytes(8, "little") + os.urandom(8)
    rng.refresh(entropy)

    out2 = rng.next(16)
    print("Output w/some entropy:", out2.hex(), "\n")

    out3 = rng.next(16)
    print("Output w/lots of entropy:", out3.hex(), "\n")
    
    print("Final state:", rng.state.hex())


if __name__ == "__main__":
    main()
