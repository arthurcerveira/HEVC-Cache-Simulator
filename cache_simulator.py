import random

from cpu_cache_simulator.CacheSim import CacheSim
from trace_processor import TraceProcessor

TRACE = './samples/mem_trace.txt'


class CacheSimulator(CacheSim):
    def __init__(self):
        super().__init__(26, 16, 6, 1, "LRU", "WT")

        trace_processor = TraceProcessor()
        self.generator = trace_processor.process_trace("samples/mem_trace.txt")

        self.dispatcher = {
            'R': None,
            'W': None
        }

    def simulate(self):
        pass


if __name__ == "__main__":
    c = CacheSimulator()
    c.simulate()
