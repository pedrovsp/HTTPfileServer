import string
import datetime
import sys

sys.path.append('gen-py')

from requestHandler.RequestHandler import *
from requestHandler.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class RqstHandler:
    #Quebra de linha
    _CRLF = '\r\n'

    def __init__(self):
        self.tree = Node("Root", None, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, [])
        self.countId = Counter(0)
        self.nodeList = NodeList([self.tree])

    def clean_resource(self, resource):
        res = resource.split("/")
        del(res[0])
        for x in res:
            if(x == ''):
                del(x)
        return res

    def do_add(self, data, path, current_node):
        nodes = self.clean_resource(path)

        if(current_node == None):
            current_node = self.tree

        if(nodes == []):
            if(current_node.data == None and data != ''):
                current_node.data = data
                return self.set_return_message(200, "ADD", current_node)
            else:
                return self.set_return_message(400, "ADD", current_node)

        if(self.search_name(current_node, nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            n_path = path.split("/", 2)
            if(len(n_path) > 2):
                n_path = "/" + n_path[2]
            else:
                n_path = ""
            return self.do_add(data, n_path, self.search_name(current_node, aux))
        else:
            self.incrementCounter()
            new_node = Node(nodes[0], None, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, self.countId.counter, [])
            self.add_child(current_node, new_node)
            aux = nodes[0]
            del(nodes[0])
            n_path = path.split("/", 2)
            if(len(n_path) > 2):
                n_path = "/" + n_path[2]
            else:
                n_path = ""
            return self.do_add(data, n_path, self.search_name(current_node, aux))

    def do_get(self, path):
        nodes = self.clean_resource(path)

        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(self.search_name(current_node, nodes[counter]) != None):
                current_node = self.search_name(current_node, nodes[counter])
                counter += 1
            else:
                return self.set_return_message(404, "GET", current_node)

        if(current_node.data != None):
            return self.set_return_message(200, "GET", current_node)
        else:
            return self.set_return_message(404, "GET", current_node)

    def do_update(self, data, path, current_node):
        nodes = self.clean_resource(path)

        if(current_node == None):
            current_node = self.tree

        if(nodes == []):
            if(current_node.data != None and data != ''):
                self.alter_data(current_node, data)
                return self.set_return_message(200, "UPDATE", current_node)
            else:
                return self.set_return_message(400, "UPDATE", current_node)

        if(self.search_name(current_node, nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            n_path = path.split("/", 2)
            if(len(n_path) > 2):
                n_path = "/" + n_path[2]
            else:
                n_path = ""
            return self.do_update(data, n_path, self.search_name(current_node, aux))
        else:
            self.set_return_message(404, "UPDATE", current_node)

    def do_update_version(self, data, version, path, current_node):
        nodes = self.clean_resource(path)

        if(current_node == None):
            current_node = self.tree

        if(nodes == []):
            if(current_node.data != None and data != '' and current_node.version == version):
                self.alter_data(current_node, data)
                return self.set_return_message(200, "UPDATE+VERSION", current_node)
            else:
                return self.set_return_message(400, "UPDATE+VERSION", current_node)

        if(self.search_name(current_node, nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            n_path = path.split("/", 2)
            if(len(n_path) > 2):
                n_path = "/" + n_path[2]
            else:
                n_path = ""
            return self.do_update_version(data, version, n_path, self.search_name(current_node, aux))
        else:
            return self.set_return_message(404, "UPDATE+VERSION", current_node)

    def do_delete(self, path):
        nodes = self.clean_resource(path)
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(self.search_name(current_node, nodes[counter]) != None):
                if(counter == len(nodes) - 1):
                    break;
                current_node = self.search_name(current_node, nodes[counter])
                counter += 1
            else:
                return self.set_return_message(404, "DELETE", current_node)

        self.delete_child(current_node, self.search_name(current_node, nodes[counter]))
        return self.set_return_message(200, "DELETE", current_node)

    def do_delete_version(self, path, version):
        nodes = self.clean_resource(path)
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(self.search_name(current_node, nodes[counter]) != None):
                if(counter == len(nodes) - 1):
                    break;
                current_node = self.search_name(current_node, nodes[counter])
                counter += 1
            else:
                return self.set_return_message(404, "DELETE+VERSION", current_node)

        if(self.search_name(current_node, nodes[counter]).version != int(version)):
            return self.set_return_message(400, "DELETE+VERSION", current_node)

        self.delete_child(current_node, self.search_name(current_node, nodes[counter]))
        return self.set_return_message(200, "VERSION", current_node)

    def do_list(self, path):
        nodes = self.clean_resource(path)
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(self.search_name(current_node, nodes[counter]) != None):
                current_node = self.search_name(current_node, nodes[counter])
                counter += 1
            else:
                return self.set_return_message(404, "LIST", current_node)

        if(current_node.children != None):
            return self.set_return_message(200, "LIST", current_node)
        else:
            return self.set_return_message(404, "LIST", current_node)

    def incrementCounter(self):
        self.countId.counter += 1

    def add_child(self, node, child):
        node.children.append(self.countId.counter)
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        self.nodeList.lista.append(child)
        return node

    def add_data(self, node, data):
        node.data = data
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def delete_child(self, node, child):
        nid = 0
        for listN in self.nodeList.lista:
            if(listN == child):
                nid = child.id
        node.children.remove(nid)
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def search_name(self, node, name):
        aux = 0
        while(aux < len(node.children)):
            if(self.getNodeById(node.children[aux]).name == name):
                return self.getNodeById(node.children[aux])
            aux += 1;
        return None

    def alter_data(self, node, data):
        node.data = data
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def get_children(self, node, returnList):
        for child in node.children:
            returnList.append(self.getNodeById(child).name)
            self.get_children(self.getNodeById(child), returnList)

        return returnList

    def getNodeById(self, nid):
        for listN in self.nodeList.lista:
            if(listN.id == nid):
                return listN

    def set_return_message(self, ret_request, request, node):
        message = ''
        if request == "ADD":
            if(ret_request == 200):
                l1 = "ADD 200 OK"# + self._CRLF
                l2 = "Version:  " + str(node.version) #+ self._CRLF
                l3 = "Creation:  " + node.creation #+ self._CRLF
                l4 = "Modification:  " + node.modification #+ self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "ADD 400 Empty Body or File Already Exists"
            return message
        elif request == "GET":
            if(ret_request == 200):
                l1 = "GET 200 OK"# + self._CRLF
                l2 = "Version:  " + str(node.version)# + self._CRLF
                l3 = "Creation:  " + node.creation# + self._CRLF
                l4 = "Modification:  " + node.modification# + self._CRLF
                message = l1+l2+l3+l4+node.data
            elif(ret_request == 404):
                message = "GET 404 File not found"
            return message
        elif request == "UPDATE":
            if(ret_request == 200):
                l1 = "UPDATE 200 OK"# + self._CRLF
                l2 = "Version:  " + str(node.version)# + self._CRLF
                l3 = "Creation:  " + node.creation# + self._CRLF
                l4 = "Modification:  " + node.modification# + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "UPDATE 400" + " Empty Body or File Doen't Exists"
            elif(ret_request == 404):
                message = "UPDATE 404 Invalid path"
            return message
        elif request == "DELETE":
            if(ret_request == 200):
                message = "DELETE 200 OK"# + self._CRLF
            elif(ret_request == 404):
                message = "DELETE 404 File not found"
            return message
        elif request == "LIST":
            if(ret_request == 200):
                l1 = "LIST 200 OK"# + self._CRLF
                l2 = "Children:  " + str(self.get_children(node, []))# + self._CRLF
                message = l1+l2
            elif(ret_request == 404):
                message = "LIST 404 Node not found"
            return message
        elif request == "DELETE+VERSION":
            if(ret_request == 200):
                message = "DELETE+VERSION 200 OK"# + self._CRLF
            elif(ret_request == 404):
                message = "DELETE+VERSION 404 File not found"
            elif(ret_request == 403):
                message = "DELETE+VERSION 403 Invalid version"
            return message
        elif request == "UPDATE+VERSION":
            if(ret_request == 200):
                l1 = "UPDATE+VERSION 200 OK"# + self._CRLF
                l2 = "Version:  " + str(node.version)# + self._CRLF
                l3 = "Creation:  " + node.creation# + self._CRLF
                l4 = "Modification:  " + node.modification# + self._CRLF
                message = l1+l2+l3+l4
            elif(ret_request == 400):
                message = "PUT 400 Empty Body or File Doen't Exists or Version Invalid"
            elif(ret_request == 404):
                message = "PUT 404 Invalid path"
            return message
        else:
            print("\n Invalid Method\n")
            return
