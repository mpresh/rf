import os
import sys

from twisted.internet import reactor, defer, task
from twisted.web import client

import simplejson as json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import settings
filename = settings.FIFO

def stop(fifo_writer_fd):
    os.close(fifo_writer_fd)
    os.remove(filename)

    print "Stopping Reactor"
    reactor.stop()

def add_data(fifo_fd):
    dict = {}
    dict["cmd"] = "twitter_user_info"
    data = {}
    dict["data"] = data

    try:
        for url in ["http://www.cnn.com", "http://www.nba.com", "http://www.nfl.com"]:
            # write stuff to fifo
            dict["data"]["url"] = url
            data = json.dumps(dict) + "\n"
            written = os.write(fifo_fd, data)
            print "Wrote:", written, len(data), data
    except Exception as e:
        stop(fifo_fd)

def consume_urls(fifo):
    while True:
        try:
            line = fifo.readline()
        except Exception as e:
            print "notta"
            return

        print "line", line

        if not line.strip():
            return

def run(fifo_writer_fd):
    # setup looping call to add urls to queue
    lcall = task.LoopingCall(add_data, fifo_writer_fd) 
    lcall.start(5)

    # consume urls
    #lcall = task.LoopingCall(consume_urls, fifo_reader) 
    #lcall.start(1)    

def main():

    try:
        print "Creating Pipe, blocking ....."
        fifo_writer_fd = os.open(settings.FIFO, os.O_WRONLY)
    except OSError, e:
        print "Filed to open writer into FIFO."
        sys.exit(1)


    #reactor.callLater(20, stop, fifo_writer)    
    reactor.callWhenRunning(run, fifo_writer_fd)

    reactor.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
