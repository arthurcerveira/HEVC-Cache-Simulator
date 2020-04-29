from datetime import datetime

from cpu_cache_simulator.CacheSim import CacheSim
from trace_processor import TraceProcessor

TRACE = './samples/mem_trace.txt'


class CacheSimulatorHEVC(CacheSim):
    def __init__(self):
        super().__init__(26, 16, 6, 1, "LRU", "WT")

        self.trace_processor = TraceProcessor()

        self.dispatcher = {
            'R': self.read,
            'W': self.write
        }

    def simulate(self, trace_input, title, width, height, encoder_cfg):
        print(f"[{datetime.now():%H:%M:%S}] Cache simulation for {title} "
              + f"in {encoder_cfg} configuration.")

        self.write_first_frame(width, height)

        self.trace_processor.set_resolution(width, height)
        generator = self.trace_processor.process_trace(trace_input)

        for operations in generator:
            for operation in operations:
                key = operation[0]
                address = self.get_address(operation, width, height)

                self.dispatcher[key](address)
        
        self.printStats()

        return f"{title},{encoder_cfg},{self.hits},{self.misses}\n"

    def get_address(self, operation, width, height):
        # OP <x> <y> <frameId>
        _, x, y, frame_id = operation.split()

        frame_start_address = int(frame_id) * height * width
        address_within_frame = int(x) + (int(y) * width)

        return frame_start_address + address_within_frame

    def write(self, address):
        super().write(address, 0)

    def write_first_frame(self, video_width, video_height):
        for x in range(video_width):
            for y in range(video_height):
                address = self.get_address(
                    f'W {x} {y} 0', video_width, video_height)

                self.write(address)

    def clear(self):
        self.hits = 0
        self.misses = 0


if __name__ == "__main__":
    cache_simulator = CacheSimulatorHEVC()
    result = cache_simulator.simulate(TRACE,'BasketballDrive', 1920, 1080, 'Random Access')

    print(result)
