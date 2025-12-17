import os
from prngs import SeedlessLCG
from prngs import SeedlessRC4
from prngs import SeedlessXorshift
from visual_test import visualize_random_dots
from visual_test import visualize_wave  

def main():
    prng1 = SeedlessLCG()
    prng2 = SeedlessRC4()
    prng3 = SeedlessXorshift()
    prng1.refresh(os.urandom(8))
    prng1.refresh(os.urandom(16))

    visualize_wave(prng1, prng2, width=600, step=20, amplitude=50, baseline1=100, baseline2=300)
if __name__ == "__main__":
    main()
