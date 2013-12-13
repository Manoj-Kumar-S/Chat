from twisted.internet import protocol, reactor
from threading import Thread

class ChatThread(Thread):
    def __init__(self, nick, transport):
        Thread.__init__(self, name='chat thread')
        self.nick = nick
        self.transport = transport

    def run(self):
        while True:
            text = raw_input()
            self.transport.write(text)

class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        '''create nick and send it to the server'''
        self.nick = raw_input('Enter a nick: ').strip().lower()
        self.transport.write(self.nick)
        self.chat_thread = ChatThread(self.nick, self.transport)
        self.chat_thread.setDaemon(True)
        self.chat_thread.start()

    def dataReceived(self, message):
        print message

class ClientFactory(protocol.ClientFactory):
    def __init__(self):
        self.chat_thread = None
    
    def buildProtocol(self, addr):
        return ClientProtocol()

    def clientConnectionLost(self, connector, reason):
        print 'You have been logged out.'
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print 'Failed to connect to server. Please try again later.'
        reactor.stop()

reactor.connectTCP('localhost', 8000, ClientFactory())
reactor.run()