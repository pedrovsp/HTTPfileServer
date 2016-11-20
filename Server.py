import socket
import sys

sys.path.append('gen-py')

from requestHandler.RequestHandler import *
from requestHandler.ttypes import *

from thrift.transport   import TSocket
from thrift.transport   import TTransport
from thrift.protocol    import TBinaryProtocol
from thrift.server      import TServer
from RqstHandler        import *

host = "127.0.0.1"

socket.getaddrinfo("127.0.0.1", 5005)

handler = RqstHandler()
processor = Processor(handler)
transport = TSocket.TServerSocket(host, int(sys.argv[1]))
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print ("Starting python server...")
server.serve()
print ("Done")
