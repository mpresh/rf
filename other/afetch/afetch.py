"""
Open a tcp server connection to handle twitter data asynchronius calls.
"""

import os
import sys

from twisted.internet import reactor, defer, task, protocol
from twisted.web import client, static, server
from twisted.protocols import basic
from twisted.application import service, internet

import simplejson as json

from commands import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def printPage(data, url):
    print url

def printError(failure, url):
    print >> sys.stderr, "Error:", failure.getErrorMessage( )

def add_urls():
    print "adding urls", urls
    urls.extend(["http://www.cnn.com", "http://www.nba.com", "http://www.nfl.com"])

def stop():
    print "Stopping Reactor"
    reactor.stop()

class CacheProtocol(basic.LineReceiver):

    def _parse_command(self, command):
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
            command_func(data=obj["data"],
			username=obj["username"],
	    		conn=self, 
			mc=mc)


    def lineReceived(self, line):
        if line == 'quit':
            self.sendLine("Goodbye.")
            self.transport.loseConnection()
        else:
            print "You Said:", line
            self._parse_command(line)

    def connectionMade(self):
        print "connection made"

    def connectionLost(self, reason):
        print "conection lost"
        basic.LineReceiver.connectionLost(self)
        self.transport.loseConnection()
        


class CacheServerFactory(protocol.ServerFactory):

    protocol = CacheProtocol

    def startFactory(self):
        print "Factory started"

    def doStart(self):
        print "doStart"
        protocol.ServerFactory.doStart(self)

    def stopFactory(self):
        print "Factory stopped"


port = 5002

application = service.Application("afetch") 
fetchService = internet.TCPServer(port, CacheServerFactory())
fetchService.setServiceParent(application)

