class TraceProcessor(object):
    def __init__(self):
        self.cu_position = tuple()
        self.ref_frame = str()
        self.cu_size = str()

        self.trace_dict = {
            "U ": self.process_cu,
            "P ": self.process_pu,
            "C ": self.process_block,
            "F ": self.process_first_search,
            "CE": self.process_block_sequence
        }

    def trace_to_rw(self, trace_path):
        with open(trace_path) as trace:
            for line in trace:
                key = line[0:2]
                if key in self.trace_dict:
                    self.trace_dict[key](line)

    def process_cu(self, line):
        # U <xCU> <yCU> <size>
        _, x, y, cu_size = line.split()

        self.cu_size = cu_size
        self.cu_position = (x, y)

    def process_pu(self, line):
        # P <sizePU> <idPart> <ref_frame_id>
        _, size_pu, id_part, ref_frame = line.split()

        self.ref_frame = ref_frame

    def process_block(self, line):
        # C <xCand> <yCand>
        _, x, y = line.split()

        initial_x = int(x) + int(self.cu_position[0])
        initial_y = int(y) + int(self.cu_position[1])

        final_x = initial_x + int(self.cu_size)
        final_y = initial_y + int(self.cu_size)

        for i in range(initial_y, final_y):
            for j in range(initial_x, final_x):
                print(f"R {i} {j} {self.ref_frame}")

    def process_first_search(self, line):
        print("posição central da first search")

    def process_block_sequence(self, line):
        print("acesso a uma sequência de blocos candidatos")


if __name__ == "__main__":
    trace_processor = TraceProcessor()
    trace_processor.trace_to_rw("samples/mem_trace.txt")
