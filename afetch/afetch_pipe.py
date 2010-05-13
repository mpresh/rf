"""
Open a tcp server connection to handle twitter data asynchronius calls.
"""


import os
import sys

from twisted.internet import reactor, defer, task
from twisted.web import client
import simplejson as json

from commands import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings

filename = settings.FIFO

def printPage(data, url):
    print url

def printError(failure, url):
    print >> sys.stderr, "Error:", failure.getErrorMessage( )

def add_urls():
    print "adding urls", urls
    urls.extend(["http://www.cnn.com", "http://www.nba.com", "http://www.nfl.com"])

def parse_command(command):
    """Convert json to python object and call appropriate command."""

    try:
        obj = json.loads(command)
    except Exception as e:
        print "Command parsing failed %s." % (command)
        return

    if obj["cmd"] not in command_map:
        print "Unkown command %s." % command
        return

    else:
        command_func = command_map[obj["cmd"]]
        command_func(obj["data"])

def process_commands(fifo):
    """ Read commands from fifo. """
    print "Process Command func"
    while True:
        try:
            line = fifo.readline()
            print "Incoming Command: ", line
        except Exception as e:
            print "Error: exception while reading from fifo.", e
            return

        # exit loop if there is no command to read
        if not line.strip():
            return

        parse_command(line)

def stop(fifo_reader):
    fifo_reader.close()
    os.remove(filename)

    print "Stopping Reactor"
    reactor.stop()


def run(fifo):
    # stop after 20 seconds
    # reactor.callLater(20, stop, fifo)    

    # setup looping call to read commands from queue
    lcall = task.LoopingCall(process_commands, fifo) 
    lcall.start(5)
            

def main():

    if not os.path.exists(filename):
        print "Error: Fifo does not exist, exiting."
        sys.exit(1)

    fifo_reader_fd = os.open(filename, os.O_RDONLY | os.O_NONBLOCK)
    fifo_reader = os.fdopen(fifo_reader_fd)
    print "Reader Pipe Open.", filename

    reactor.callWhenRunning(run, fifo_reader)
    
    reactor.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
