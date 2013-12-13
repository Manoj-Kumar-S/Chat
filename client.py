from twisted.internet.protocol import ClientFactory, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from threading import Thread

class ChatThread(Thread):
    def __init__(self, name, protocol):
        Thread.__init__(self)
        self.name = name
        self.protocol = protocol
        
    def run(self):
        while True:
            text = raw_input()
            self.protocol.sendLine(text)

class ClientProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        print 'client has connected to the server'
    
    def lineReceived(self, line):
        if line == 'What is your name?':
            self.name = raw_input('Enter your username: ').strip()
            self.sendLine(self.name)
            ChatThread(self.name, self).start()
        else:
            print line

class ClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ClientProtocol(self)
    
    def clientConnectionFailed(self, connector, reason):
        print 'connection failed: ' + str(reason.getErrorMessage())
    
    def clientConnectionLost(self, connector, reason):
        print 'connection lost: ' + str(reason.getErrorMessage())
    
reactor.connectTCP('localhost', 8000, ClientFactory())
reactor.run()
