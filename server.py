from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = 'REGISTER'
    
    def connectionMade(self):
        print 'Client connected'
        
    def connectionLost(self, reason):
        self.broadcastMessage('%s has left the chatroom!' % (self.name))
    
    def lineReceived(self, line):
        if self.state == 'REGISTER':
            self.handle_register(line)
        else:
            self.handle_chat(line)

    def handle_register(self, name):
        if name in self.factory.users:
            self.sendLine('* Nick already in use. Try another nick. *')
            return
        else:
            self.name = name
            self.factory.users[self.name] = self
            self.sendLine('* Welcome %s! *' % (self.name))
            self.broadcastMessage('* %s has joined the chat *' % (self.name,))
            self.state = 'CHAT'
            
    def handle_chat(self, chat):
        self.broadcastMessage('<%s>: %s' % (self.name, chat))
        
    def broadcastMessage(self, chat):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:
                protocol.sendLine(chat)
                
class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(8000, ChatFactory())
print 'Server is running and listening for incoming connections...'
reactor.run()