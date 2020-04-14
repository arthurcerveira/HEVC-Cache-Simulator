import random

from cpu_cache_simulator.CacheSim import CacheSim
from trace_processor import TraceProcessor

TRACE = './samples/mem_trace.txt'


class CacheSimulatorHEVC(CacheSim):
    def __init__(self):
        super().__init__(26, 16, 6, 1, "LRU", "WT")

        trace_processor = TraceProcessor()
        self.generator = trace_processor.process_trace("samples/mem_trace.txt")

        self.video_height = 1080
        self.video_width = 1920

        self.dispatcher = {
            'R': self.read,
            'W': self.write
        }

    def simulate(self):
        self.write_first_frame()

        for operations in self.generator:
            for operation in operations:
                key = operation[0]
                address = self.get_address(operation)

                self.dispatcher[key](address)

    def get_address(self, operation):
        # OP <x> <y> <frameId>
        _, x, y, frame_id = operation.split()

        frame_start_address = int(frame_id) * \
            self.video_height * self.video_width
        address_within_frame = int(x) + (int(y) * self.video_width)

        address = frame_start_address + address_within_frame
        if address < 0:
            print(address)

        return frame_start_address + address_within_frame

    def write(self, address):
        super().write(address, 0)

    def write_first_frame(self):
        for x in range(self.video_width):
            for y in range(self.video_height):
                address = self.get_address(f'W {x} {y} 0')

                self.write(address)


if __name__ == "__main__":
    cache_simulator = CacheSimulatorHEVC()
    cache_simulator.simulate()
    cache_simulator.printStats()
