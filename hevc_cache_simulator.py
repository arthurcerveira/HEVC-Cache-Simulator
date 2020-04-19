from cpu_cache_simulator.CacheSim import CacheSim
from trace_processor import TraceProcessor

TRACE = './samples/mem_trace.txt'


class CacheSimulatorHEVC(CacheSim):
    def __init__(self):
        super().__init__(26, 16, 6, 1, "LRU", "WT")

        self.trace_processor = TraceProcessor()

        self.video_height = int()
        self.video_width = int()

        self.dispatcher = {
            'R': self.read,
            'W': self.write
        }

    def simulate(self, title, width, height, video_cfg):
        self.write_first_frame(width, height)

        self.trace_processor.set_resolution(width, height)
        generator = self.trace_processor.process_trace("samples/mem_trace.txt")

        for operations in generator:
            for operation in operations:
                key = operation[0]
                address = self.get_address(operation)

                self.dispatcher[key](address)

        return f"{title};{video_cfg};{self.hits};{self.misses}"

    def get_address(self, operation):
        # OP <x> <y> <frameId>
        _, x, y, frame_id = operation.split()

        frame_start_address = int(frame_id) * \
            self.video_height * self.video_width
        address_within_frame = int(x) + (int(y) * self.video_width)

        return frame_start_address + address_within_frame

    def write(self, address):
        super().write(address, 0)

    def write_first_frame(self, video_width, video_height):
        for x in range(video_width):
            for y in range(video_height):
                address = self.get_address(f'W {x} {y} 0')

                self.write(address)


if __name__ == "__main__":
    cache_simulator = CacheSimulatorHEVC()
    cache_simulator.simulate('BasketballDrive', 1920, 1080, 'Random Access')
    cache_simulator.printStats()
