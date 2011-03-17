'''
Created on 16. mars 2011

@author: magnuswestergaard
'''
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
import sys

class PubeBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        if self.nickname in msg:
            self.msg(self.factory.channel, "DERP!")

class PubeBotFactory(protocol.ClientFactory):
    protocol = PubeBot

    def __init__(self, channel, nickname='pubes'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

if __name__ == "__main__":
    try:
        chan = sys.argv[1]
    except IndexError:
        print "Usage:"
        print "  python pubes.py labcrab"
    reactor.connectTCP('irc.freenode.net', 6667, PubeBotFactory('#' + chan,
        'pubesbot'))
    reactor.run()

