TRACE_DICT = {
    "U ": "início da codificação de uma CU",
    "P ": "processamento de uma PU",
    "C ": "acesso a um bloco candidato",
    "F ": "posição central da first search",
    "CE": "acesso a uma sequência de blocos candidatos"
}


def trace_to_rw(trace_path):
    with open(trace_path) as trace:
        for line in trace:
            key = line[0:2]
            if key in TRACE_DICT:
                print(TRACE_DICT[key])


if __name__ == "__main__":
    trace_to_rw("samples/mem_trace.txt")
