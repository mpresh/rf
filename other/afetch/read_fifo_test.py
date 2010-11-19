import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings

filename = settings.FIFO

fifo_reader_fd = os.open(filename, os.O_RDONLY)
f = os.fdopen(fifo_reader_fd)

print "opened fd", filename

while True:

    #print "reading data"
    #r = os.read(fifo_reader_fd, 10)
    line = f.readline()
    if line.strip():
        sys.stdout.write(line)
