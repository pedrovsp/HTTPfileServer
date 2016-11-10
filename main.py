import sys
import Server

port = int(sys.argv[1])

server = Server.Server()
server.start(port)
