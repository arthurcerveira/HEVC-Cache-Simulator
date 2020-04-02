PARTITION_PU = {
    '0': ([1, 1],     [1, 1]),      # 2N X 2N
    '1': ([1, 0.5],   [1, 0.5]),    # 2N X N
    '2': ([0.5, 1],   [0.5, 1]),    # N X 2N
    '3': ([0.5, 0.5], [0.5, 0.5]),  # N X N
    '4': ([1, 0.75],  [1, 0.25]),   # 2N x nU
    '5': ([1, 0.25],  [1, 0.75]),   # 2N x nD
    '6': ([0.25, 1],  [0.75, 1]),   # nL x 2N
    '7': ([0.75, 1],  [0.25, 1])    # nR x 2N
}

INITIAL_CU_SHIFT = {
    '0': ([0, 0],   [0, 0]),      # 2N X 2N
    '1': ([0, 0],   [0, 0.5]),    # 2N X N
    '2': ([0, 0],   [0.5, 0]),    # N X 2N
    '3': ([0, 0],   [0.5, 0],
          [0, 0.5], [0.5, 0.5]),  # N X N
    '4': ([0, 0],   [0, 0.75]),   # 2N x nU
    '5': ([0, 0],   [0, 0.25]),   # 2N x nD
    '6': ([0, 0],   [0.25, 0]),   # nL x 2N
    '7': ([0, 0],   [0.75, 0])    # nR x 2N
}


class TraceProcessor(object):
    def __init__(self):
        self.cu_position = tuple()
        self.ref_frame = str()
        self.cu_size = int()
        self.cu_current_cu_width = int()

        self.trace_dict = {
            "U ": self.process_cu,
            "P ": self.process_pu,
            "C ": self.process_block,
            "F ": self.process_first_search,
            "CE": self.process_block_sequence
        }

    def process_trace(self, trace_path):
        with open(trace_path) as trace:
            for line in trace:
                key = line[0:2]
                if key in self.trace_dict:
                    self.trace_dict[key](line)

    def process_cu(self, line):
        # U <xCU> <yCU> <size>
        _, x, y, cu_size = line.split()

        self.cu_size = int(cu_size)
        self.cu_position = (int(x), int(y))

    def process_pu(self, line):
        # P <sizePU> <idPart> <ref_frame_id>
        _, size_pu, id_part, ref_frame = line.split()

        self.ref_frame = ref_frame

        partition_hor, partition_ver = PARTITION_PU[size_pu][int(id_part)]

        self.current_cu_width = partition_hor * self.cu_size
        self.current_cu_height = partition_ver * self.cu_size

        self.shift_cu_position(size_pu, id_part)

    def process_block(self, line):
        # C <xCand> <yCand>
        _, x, y = line.split()

        initial_x = int(x) + int(self.cu_position[0])
        initial_y = int(y) + int(self.cu_position[1])

        final_x = initial_x + self.current_cu_width
        final_y = initial_y + self.current_cu_height

        for i in range(initial_y, final_y):
            for j in range(initial_x, final_x):
                print(f"R {i} {j} {self.ref_frame}")

    def process_first_search(self, line):
        pass
        # print("posição central da first search")

    def process_block_sequence(self, line):
        pass
        # print("acesso a uma sequência de blocos candidatos")

    def shift_cu_position(self, size_pu, id_part):
        x, y = self.cu_position

        x_shift, y_shift = INITIAL_CU_SHIFT[size_pu][int(id_part)]

        x = x + int(x_shift) * self.cu_size
        y = y + int(y_shift) * self.cu_size

        self.cu_position = (x, y)


if __name__ == "__main__":
    trace_processor = TraceProcessor()
    trace_processor.process_trace("samples/mem_trace.txt")
