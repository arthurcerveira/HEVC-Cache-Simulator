import argparse
import random
from .cache import Cache
from .memory import Memory


class CacheSim:
    def __init__(self, memory, cache, block, mapping, replace, write):
        self.memSize = 2 ** memory
        self.cacheSize = 2 ** cache
        self.blockSize = 2 ** block
        self.mapping = 2 ** mapping
        self.replacementPolicy = replace
        self.writePolicy = write

        self.memory = Memory(self.memSize, self.blockSize)
        self.cache = Cache(self.cacheSize, self.memSize, self.blockSize,
                           self.mapping, self.replacementPolicy, self.writePolicy)

        self.hits = 0
        self.misses = 0

        self.__reportConfiguration()

    def __reportConfiguration(self):
        mapping_str = "{0}-way associative".format(self.mapping)
        print("\nMemory size: " + str(self.memSize) +
              " bytes (" + str(self.memSize // self.blockSize) + " blocks)")
        print("Cache size: " + str(self.cacheSize) +
              " bytes (" + str(self.cacheSize // self.blockSize) + " lines)")
        print("Block size: " + str(self.blockSize) + " bytes")
        print("Mapping policy: " +
              ("direct" if self.mapping == 1 else mapping_str) + "\n")

    def read(self, address):
        """Read a byte from cache."""
        cache_block = self.cache.read(address)

        if cache_block:
            self.hits += 1
        else:
            block = self.memory.get_block(address)
            victim_info = self.cache.load(address, block)
            cache_block = self.cache.read(address)

            self.misses += 1

            # Write victim line's block to memory if replaced
            if victim_info:
                self.memory.set_block(victim_info[0], victim_info[1])

        return cache_block[self.cache.get_offset(address)]

    def write(self, address, byte):
        """Write a byte to cache."""
        written = self.cache.write(address, byte)

        if written:
            self.hits += 1
        else:
            self.misses += 1

        if self.writePolicy == Cache.WRITE_THROUGH:
            # Write block to memory
            block = self.memory.get_block(address)
            block[self.cache.get_offset(address)] = byte
            self.memory.set_block(address, block)
        elif self.writePolicy == Cache.WRITE_BACK:
            if not written:
                # Write block to cache
                block = self.memory.get_block(address)
                self.cache.load(address, block)
                self.cache.write(address, byte)

    def printStats(self):
        ratio = (self.hits / ((self.hits + self.misses)
                              if self.misses else 1)) * 100

        print("\nHits: {0} | Misses: {1}".format(self.hits, self.misses))
        print("Hit/Miss Ratio: {0:.2f}%".format(ratio) + "\n")

    def getMemSize(self):
        return self.memSize


# just for test...
if __name__ == "__main__":
    sim = CacheSim(25, 16, 6, 2, "RAND", "WT")
    N_ACCESS = 1000000
    for i in range(N_ACCESS):
        address = random.randint(0, sim.getMemSize() - 1)
        #address = i % sim.getMemSize()
        sim.read(address)
    sim.printStats()
