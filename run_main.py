import os
from lcg import SeedlessLCG
from visual_test import visualize_random_pattern

def main():
    prng = SeedlessLCG()
    prng.refresh(os.urandom(8))
    visualize_random_pattern(prng, width=550, height=600)

if __name__ == "__main__":
    main()
