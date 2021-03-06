from twisted.internet import protocol, reactor
from threading import Thread
from common.message import message
import cPickle as pickle

class ChatThread(Thread):
    def __init__(self, nick, transport):
        Thread.__init__(self, name='chat thread')
        self.nick = nick
        self.transport = transport
        self.current_user = None
        
    def run(self):
        while True:
            text = raw_input().strip()
            if text.startswith('~'):
                text_message = None
                try:
                    '''for commands that have a tag; for eg. ~man ping'''
                    command, user = text[1:].split()
                    text_message = message.CommandMessage(command, user)
                except ValueError as e:
                    '''command that do not have a tag; for eg. ~other'''
                    command = text[1:]
                    text_message = message.CommandMessage(command)
            else:
                text_message = message.ChatMessage(self.nick, text)
            self.transport.write(pickle.dumps(text_message))

class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        '''create nick and send it to the server'''
        while True:
            nick = raw_input('Enter a nick: ').strip().lower()
            if ' ' in nick:
                print '* Only single-word nicks are allowed. *'
            else: break
        self.nick = nick
        self.transport.write(self.nick)
        self.chat_thread = ChatThread(self.nick, self.transport)
        self.chat_thread.setDaemon(True)
        self.chat_thread.start()
    
    def dataReceived(self, data):
        chat_message = pickle.loads(data)
        '''get the status of the message and see how to parse it'''
        status = chat_message.get_status()
        if status == 'SERVER_MESSAGE':
            print '* %s *' % (chat_message.get_text())
        elif status == 'CHAT_MESSAGE':
            sender = chat_message.get_sender()
            text = chat_message.get_text()
            output = '<%s>: %s' % (sender, text)
            print output
    
class ClientFactory(protocol.ClientFactory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return ClientProtocol()
    
    def clientConnectionLost(self, connector, reason):
        print 'You have been logged out.'
        reactor.stop()
    
    def clientConnectionFailed(self, connector, reason):
        print 'Failed to connect to server.'
        reactor.stop()

reactor.connectTCP('localhost', 8001, ClientFactory())
reactor.run()