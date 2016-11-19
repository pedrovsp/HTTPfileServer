import sys
from Server import *

port = int(sys.argv[1])

server = Server()
server.start(port)
