import socket
import RequestHandler
import threading
import Node
import _thread

class Server(object):

    host = "127.0.0.1"

    def start(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        self.handler = RequestHandler.RequestHandler()

        print ("\nServer started")

        while 1:
            print ("\n----> Waiting Connection\n\n")
            (con, addr) = self.sock.accept()

            _thread.start_new_thread(self.handler.run, (con, ))
