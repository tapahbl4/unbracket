def read(path):
    f = open(path, 'r')
    for line in f:
        if len(line.strip()) > 0:
            yield line.strip()
    f.close()
