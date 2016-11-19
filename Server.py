import socket
import sys

sys.path.append('gen-py')

from requestHandler.RequestHandler import *
from requestHandler.ttypes import *

from thrift.transport   import TSocket
from thrift.transport   import TTransport
from thrift.protocol    import TBinaryProtocol
from thrift.server      import TServer

from RequestHandler import *

class Server(object):

    host = "127.0.0.1"

    def start(self, portrcv):
        self.handler = RequestHandler()
        self.processor = Server.Processor(handler)
        self.transport = TSocket.TServerSocket(port=portrcv)
        self.tfactory = TTransport.TBufferedTransportFactory()
        self.pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

        print ("\nServer started")
