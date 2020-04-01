class TraceProcessor(object):
    def __init__(self):
        self.cu_position = tuple([0, 0])
        self.ref_frame = str()

        self.TRACE_DICT = {
            "U ": self.process_cu,
            "P ": self.process_pu,
            "C ": self.process_block,
            "F ": self.process_first_search,
            "CE": self.process_block_sequence
        }

    def trace_to_rw(self, trace_path):
        i = 0

        with open(trace_path) as trace:
            for line in trace:
                key = line[0:2]
                if key in self.TRACE_DICT:
                    self.TRACE_DICT[key](line)

                if i == 50:
                    break
                i += 1

    def process_pu(self, line):
        print("processamento de uma PU")

    def process_cu(self, line):
        print("início da codificação de uma CU")

    def process_block(self, line):
        print("acesso a um bloco candidato")

    def process_first_search(self, line):
        print("posição central da first search")

    def process_block_sequence(self, line):
        print("acesso a uma sequência de blocos candidatos")


if __name__ == "__main__":
    trace_processor = TraceProcessor()
    trace_processor.trace_to_rw("samples/mem_trace.txt")
