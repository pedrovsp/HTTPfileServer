import string
import Node
import time
import threading
import re

class RequestHandler(threading.Thread):
    #Quebra de linha
    _CRLF = '\r\n'

    #Sucesso
    _200 = 200

    #Caminho não encontrado
    _404 = 404

    def __init__(self):
        threading.Thread.__init__(self)
        self.tree = Node.Node("Root", None)

    def run(self, connection):

        try:
            print ("!---------- New Connection ----------!\n")

            message = connection.recv(1024)

            if not message:
                return

            #[0] = Request Line; [1] = Head; [2] = Body
            (requestLine, header, body) = self.split_request(message)

            (method, resource, version) = self.get_request_line_info(requestLine)

            if(version != 1.1):
                print("\n You must use HTTP/1.1\n")
                return

            nodes = self.clean_resource(resource)

            if method == "POST":
                (x, node) = self.do_post(self.tree, nodes, body)
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "GET":
                (x, node) = self.do_get(nodes)
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "PUT":
                (x, node) = self.do_put(self.tree, nodes, body)
                return_message = self.set_return_message(x, method, node)
                return_message = "HTTP/1.1 " + return_message
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "HEAD":
                (x, node) = self.do_head(nodes)
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "DELETE":
                (x, node) = self.do_delete(nodes)
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "LIST":
                (x, node) = self.do_list(nodes)
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif re.match("DELETE\+[0-9]+", method):
                version = method.split("+")
                (x, node) = self.do_delete_version(nodes, version[1])
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif re.match("UPDATE\+[0-9]+", method):
                version = method.split("+")
                (x, node) = self.do_update_version(self.tree, nodes, body, version[1])
                return_message = self.set_return_message(x, method, node)
                return_message = "HTTP/1.1 " + return_message
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "ADD":
                (x, node) = self.do_post(self.tree, nodes, body)
                return_message = self.set_return_message(x, method, node)
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            elif method == "UPDATE":
                (x, node) = self.do_put(self.tree, nodes, body)
                return_message = self.set_return_message(x, method, node)
                return_message = return_message
                print(requestLine)
                print(header)
                print(body)
                print("-----------> Response message")
                print(return_message)
                connection.sendall(b'%s' % return_message.encode('utf-8'))
                return
            else:
                print("\n Invalid Method\n")
                return

        finally:
            connection.close()

    def do_post(self, tree, nodes, data):
        tree.lock.acquire()
        if(nodes == []):
            if(tree.data == None and data != ''):
                tree.data = data
                tree.lock.release()
                return (200, tree)
            else:
                tree.lock.release()
                return (400, None)

        if(tree.search_name(nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            tree.lock.release()
            return self.do_post(tree.search_name(aux), nodes, data)
        else:
            new_node = Node.Node(nodes[0], None)
            tree.add_child(new_node)
            aux = nodes[0]
            del(nodes[0])
            tree.lock.release()
            return self.do_post(tree.search_name(aux), nodes, data)

    def do_get(self, nodes):
        current_node = self.tree
        current_node.lock.acquire()
        counter = 0

        while(counter < len(nodes)):
            if(current_node.search_name(nodes[counter]) != None):
                current_node.lock.release()
                current_node = current_node.search_name(nodes[counter])
                current_node.lock.acquire()
                counter += 1
            else:
                current_node.lock.release()
                return (404, None)

        if(current_node.data != None):
            current_node.lock.release()
            return (200, current_node)
        else:
            current_node.lock.release()
            return (404, None)

    def do_put(self, tree, nodes, data):
        tree.lock.acquire()
        if(nodes == []):
            if(tree.data != None and data != ''):
                tree.alter_data(data)
                tree.lock.release()
                return (200, tree)
            else:
                tree.lock.release()
                return (400, None)

        if(tree.search_name(nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            tree.lock.release()
            return self.do_put(tree.search_name(aux), nodes, data)
        else:
            tree.lock.release()
            return (404, None)

    def do_update_version(self, tree, nodes, data, version):
        tree.lock.acquire()
        print(tree.version)
        print(int(version))
        if(nodes == []):
            if(tree.data != None and data != '' and tree.version == int(version)):
                tree.alter_data(data)
                tree.lock.release()
                return (200, tree)
            else:
                tree.lock.release()
                return (400, None)

        if(tree.search_name(nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            tree.lock.release()
            return self.do_update_version(tree.search_name(aux), nodes, data, version)
        else:
            tree.lock.release()
            return (404, None)

    def do_delete(self, nodes):
        current_node = self.tree
        current_node.lock.acquire()
        counter = 0

        while(counter < len(nodes)):
            if(current_node.search_name(nodes[counter]) != None):
                if(counter == len(nodes) - 1):
                    break;
                current_node.lock.release()
                current_node = current_node.search_name(nodes[counter])
                current_node.lock.acquire()
                counter += 1
            else:
                current_node.lock.release()
                return (404, None)

        current_node.delete_child(current_node.search_name(nodes[counter]))
        current_node.lock.release()
        return (200, None)

    def do_delete_version(self, nodes, version):
        current_node = self.tree
        current_node.lock.acquire()
        counter = 0

        while(counter < len(nodes)):
            if(current_node.search_name(nodes[counter]) != None):
                if(counter == len(nodes) - 1):
                    break;
                current_node.lock.release()
                current_node = current_node.search_name(nodes[counter])
                current_node.lock.acquire()
                counter += 1
            else:
                current_node.lock.release()
                return (404, None)

        if(current_node.search_name(nodes[counter]).version != int(version)):
            return (403, None)

        current_node.delete_child(current_node.search_name(nodes[counter]))
        current_node.lock.release()
        return (200, None)

    def do_head(self, nodes):
        current_node = self.tree
        current_node.lock.acquire()
        counter = 0

        while(counter < len(nodes)):
            if(current_node.search_name(nodes[counter]) != None):
                current_node.lock.release()
                current_node = current_node.search_name(nodes[counter])
                current_node.lock.acquire()
                counter += 1
            else:
                current_node.lock.release()
                return (404, None)

        if(current_node.data != None):
            current_node.lock.release()
            return (200, current_node)
        else:
            current_node.lock.release()
            return (404, None)

    def do_list(self, nodes):
        current_node = self.tree
        current_node.lock.acquire()
        counter = 0

        while(counter < len(nodes)):
            if(current_node.search_name(nodes[counter]) != None):
                current_node.lock.release()
                current_node = current_node.search_name(nodes[counter])
                current_node.lock.acquire()
                counter += 1
            else:
                current_node.lock.release()
                return (404, None)

        if(current_node.children != None):
            current_node.lock.release()
            return (200, current_node)
        else:
            current_node.lock.release()
            return (404, None)

    def split_request(self, message):
        splitted = message.decode("utf-8").split(self._CRLF, 1)
        rqst_line = splitted[0]
        headAndBody = splitted[1]
        splitted = headAndBody.split(self._CRLF + self._CRLF, 1)
        #[0] = Request Line; [1] = Head; [2] = Body
        return rqst_line, splitted[0], splitted[1]

    def get_request_line_info(self, httpLine):
        splitted = httpLine.split(' ')
        #[0] = Type; [1] = URI; [2] = Versionfloat(splitted[2].split('/')[1])
        return splitted[0], splitted[1], float(splitted[2].split('/')[1])

    def clean_resource(self, resource):
        res = resource.split("/")
        del(res[0])
        for x in res:
            if(x == ''):
                del(x)
        return res

    def set_return_message(self, ret_request, request, node):
        message = ''
        if request == "POST":
            if(ret_request == 200):
                l1 = "POST 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "POST 400 Empty Body or File Already Exists"
            return message
        if request == "ADD":
            if(ret_request == 200):
                l1 = "ADD 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "ADD 400 Empty Body or File Already Exists"
            return message
        elif request == "GET":
            if(ret_request == 200):
                l1 = "GET 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4+node.data
            elif(ret_request == 404):
                message = "GET 404 File not found"
            return message
        elif request == "PUT":
            if(ret_request == 200):
                l1 = "PUT 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "PUT 400 Empty Body or File Doen't Exists"
            elif(ret_request == 404):
                message = "PUT 404 Invalid path"
            return message
        elif request == "UPDATE":
            if(ret_request == 200):
                l1 = "UPDATE 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "UPDATE 400" + " Empty Body or File Doen't Exists"
            elif(ret_request == 404):
                message = "UPDATE 404 Invalid path"
            return message
        elif request == "HEAD":
            if(ret_request == 200):
                l1 = "HEAD 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 404):
                message = "HEAD 404 File not found"
            return message
        elif request == "DELETE":
            if(ret_request == 200):
                message = "DELETE 200 OK" + self._CRLF
            elif(ret_request == 404):
                message = "DELETE 404 File not found"
            return message
        elif request == "LIST":
            if(ret_request == 200):
                l1 = "LIST 200 OK" + self._CRLF
                l2 = "Children:  " + str(node.get_children(node, [])) + self._CRLF
                message = l1+l2
            elif(ret_request == 404):
                message = "LIST 404 Node not found"
            return message
        elif re.match("DELETE\+[0-9]+", request):
            if(ret_request == 200):
                message = "DELETE+VERSION 200 OK" + self._CRLF
            elif(ret_request == 404):
                message = "DELETE+VERSION 404 File not found"
            elif(ret_request == 403):
                message = "DELETE+VERSION 403 Invalid version"
            return message
        elif re.match("UPDATE\+[0-9]+", request):
            if(ret_request == 200):
                l1 = "UPDATE+VERSION 200 OK" + self._CRLF
                l2 = "Version:  " + str(node.version) + self._CRLF
                l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "PUT 400 Empty Body or File Doen't Exists or Version Invalid"
            elif(ret_request == 404):
                message = "PUT 404 Invalid path"
            return message
        else:
            print("\n Invalid Method\n")
            return
