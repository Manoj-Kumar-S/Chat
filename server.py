from twisted.internet import protocol, reactor

commands = ['users', 'exit']

class ChatProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.peer = None
        self.state = 'REGISTER'

    def connectionMade(self):
        self.peer = self.transport.getPeer()
        print 'Client connected from %s:%s' % (self.peer.host, self.peer.port)

    def connectionLost(self, reason):
        self.broadcastMessage('* %s has left the chatroom! *' % (self.name))
        print '<%s> disconnected at %s:%s' % (self.name, self.peer.host, self.peer.port) 

    def dataReceived(self, data):
        if self.state == 'REGISTER': self.handle_register(data)
        else: self.handle_chat(data)
    
    def handle_register(self, name):
        if name in self.factory.users:
            self.transport.write('* Nice already in use. Try another nick. *')
            return
        else:
            self.name = name
            self.factory.users[self.name] = self.transport
            self.transport.write('* Welcome %s! *\n' % (self.name))
            self.transport.write('* Use ~users to see the list of users currently online *\n')
            self.broadcastMessage('* %s has joined the chat *' % (self.name, ))
            self.state = 'CHAT'
            
    def handle_chat(self, chat):
        if chat.startswith('~'):
            command = chat[1:]
            if command == 'users':
                self.send_users_list()
            elif command == 'exit':
                self.exit_user()
        else: self.broadcastMessage('<%s>: %s' % (self.name, chat))
    
    def send_users_list(self):
        delimited_users_list = ''
        for user in self.factory.users.keys():
            delimited_users_list += user + ', '
        self.transport.write('* %s *' % (delimited_users_list[0 : len(delimited_users_list)-2]))
    
    def exit_user(self):
        self.transport.loseConnection()
        del self.factory.users[self.name]

    def broadcastMessage(self, message):
        for name, transport in self.factory.users.iteritems():
            if transport != self.transport:
                transport.write(message)

class ChatFactory(protocol.Factory):
    def __init__(self):
        self.users = {}
    
    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(8000, ChatFactory())
print 'Server running, listening for incoming connections...'
reactor.run()
        