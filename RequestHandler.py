import string
import time
import glob
import sys

sys.path.append('gen-py')
#sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from sharedService.SharedService import *
from requestHandler.RequestHandler import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class RequestHandler():
    #Quebra de linha
    _CRLF = '\r\n'

    def __init__(self):
        self.tree = NodeInit("Root", None)

    def do_post(self, nodes, data):
        if(nodes == []):
            if(tree.data == None and data != ''):
                tree.data = data
                return "Success 200"
            else:
                return "Error 404"

        if(search_name(current_node, nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            return self.do_post(search_name(current_node, aux), nodes, data)
        else:
            new_node = Node.Node(nodes[0], None)
            tree.add_child(new_node)
            aux = nodes[0]
            del(nodes[0])
            return self.do_post(tree.search_name(aux), nodes, data)

    def do_get(self, nodes):
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(search_name(current_node, nodes[counter]) != None):
                current_node = search_name(current_node, nodes[counter])
                counter += 1
            else:
                return "Error 404"

        if(current_node.data != None):
            return "Success 200"
        else:
            return "Error 404"

    def do_put(self, tree, nodes, data):
        if(nodes == []):
            if(tree.data != None and data != ''):
                alter_data(tree, data)
                return "Success 200"
            else:
                return "Error 400"

        if(search_name(tree, nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            return self.do_put(search_name(tree, aux), nodes, data)
        else:
            return "Error 404"

    def do_update_version(self, tree, nodes, data, version):
        if(nodes == []):
            if(tree.data != None and data != '' and tree.version == int(version)):
                tree.alter_data(tree, data)
                return "Success 200"
            else:
                return "Error 400"

        if(search_name(tree, nodes[0]) != None):
            aux = nodes[0]
            del(nodes[0])
            return self.do_update_version(search_name(aux), nodes, data, version)
        else:
            return "Error 404"

    def do_delete(self, nodes):
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(self.search_name(current_node, nodes[counter]) != None):
                if(counter == len(nodes) - 1):
                    break;
                current_node = self.search_name(current_node, nodes[counter])
                counter += 1
            else:
                return "Error 404"

        self.delete_child(current_node, self.search_name(current_node, nodes[counter]))
        return "Sucess 200"

    def do_delete_version(self, nodes, version):
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(search_name(current_node, nodes[counter]) != None):
                if(counter == len(nodes) - 1):
                    break;
                current_node = search_name(current_node, nodes[counter])
                counter += 1
            else:
                return "Error 404"

        if(search_name(current_node, nodes[counter]).version != int(version)):
            return "Error 403"

        delete_child(search_name(current_node, nodes[counter]))
        return "Success 200"

    def do_head(self, nodes):
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(search_name(current_node, nodes[counter]) != None):
                current_node = search_name(current_node, nodes[counter])
                counter += 1
            else:
                return "Error 404"

        if(current_node.data != None):
            return "Success 200"
            #return (200, current_node)
        else:
            return "Error 404"
            #return (404, None)

    def do_list(self, nodes):
        current_node = self.tree
        counter = 0

        while(counter < len(nodes)):
            if(search_name(current_node, nodes[counter]) != None):
                current_node = search_name(current_node, nodes[counter])
                counter += 1
            else:
                return "Error 404"
                #return (404, None)

        if(current_node.children != None):
            return "Success 200"
            #return (200, current_node)
        else:
            return "Error 404"
            #return (404, None)

    def add_child(self, node, child):
        node.children.append(child)
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def add_data(self, node, data):
        node.data = data
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def delete_child(self, node, child):
        node.children.remove(child)
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def search_name(self, node, name):
        aux = 0
        while(aux < len(node.children)):
            if(node.children[aux].name == name):
                return node.children[aux]
            aux += 1;
        return None

    def alter_data(self, node, data):
        node.data = data
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version += 1
        return node

    def get_children(self, node, returnList):
        for child in node.children:
            returnList.append(child.name)
            child.get_children(child, returnList)

        return returnList

    def NodeInit(self, name, data):
        node = None
        node.name = name
        node.data = data
        node.creation = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.modification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node.version = 0
        node.children = []
        return node

    #  def set_return_message(self, ret_request, request, node):
    #     message = ''
    #     if request == "POST":
    #         if(ret_request == 200):
    #             l1 = "POST 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4
    #         elif(ret_request == 400):
    #             message = "POST 400 Empty Body or File Already Exists"
    #         return message
    #     if request == "ADD":
    #         if(ret_request == 200):
    #             l1 = "ADD 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4
    #         elif(ret_request == 400):
    #             message = "ADD 400 Empty Body or File Already Exists"
    #         return message
    #     elif request == "GET":
    #         if(ret_request == 200):
    #             l1 = "GET 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4+node.data
    #         elif(ret_request == 404):
    #             message = "GET 404 File not found"
    #         return message
    #     elif request == "PUT":
    #         if(ret_request == 200):
    #             l1 = "PUT 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4
    #         elif(ret_request == 400):
    #             message = "PUT 400 Empty Body or File Doen't Exists"
    #         elif(ret_request == 404):
    #             message = "PUT 404 Invalid path"
    #         return message
    #     elif request == "UPDATE":
    #         if(ret_request == 200):
    #             l1 = "UPDATE 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4
    #         elif(ret_request == 400):
    #             message = "UPDATE 400" + " Empty Body or File Doen't Exists"
    #         elif(ret_request == 404):
    #             message = "UPDATE 404 Invalid path"
    #         return message
    #     elif request == "HEAD":
    #         if(ret_request == 200):
    #             l1 = "HEAD 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4
    #         elif(ret_request == 404):
    #             message = "HEAD 404 File not found"
    #         return message
    #     elif request == "DELETE":
    #         if(ret_request == 200):
    #             message = "DELETE 200 OK" + self._CRLF
    #         elif(ret_request == 404):
    #             message = "DELETE 404 File not found"
    #         return message
    #     elif request == "LIST":
    #         if(ret_request == 200):
    #             l1 = "LIST 200 OK" + self._CRLF
    #             l2 = "Children:  " + str(node.get_children(node, [])) + self._CRLF
    #             message = l1+l2
    #         elif(ret_request == 404):
    #             message = "LIST 404 Node not found"
    #         return message
    #     elif re.match("DELETE\+[0-9]+", request):
    #         if(ret_request == 200):
    #             message = "DELETE+VERSION 200 OK" + self._CRLF
    #         elif(ret_request == 404):
    #             message = "DELETE+VERSION 404 File not found"
    #         elif(ret_request == 403):
    #             message = "DELETE+VERSION 403 Invalid version"
    #         return message
    #     elif re.match("UPDATE\+[0-9]+", request):
    #         if(ret_request == 200):
    #             l1 = "UPDATE+VERSION 200 OK" + self._CRLF
    #             l2 = "Version:  " + str(node.version) + self._CRLF
    #             l3 = "Creation:  " + node.creation.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             l4 = "Modification:  " + node.modification.strftime("%Y-%m-%d %H:%M:%S") + self._CRLF
    #             message = l1+l2+l3+l4
    #         elif(ret_request == 400):
    #             message = "PUT 400 Empty Body or File Doen't Exists or Version Invalid"
    #         elif(ret_request == 404):
    #             message = "PUT 404 Invalid path"
    #         return message
    #     else:
    #         print("\n Invalid Method\n")
    #         return
