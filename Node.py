import datetime

class Node():
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.creation = datetime.datetime.now()
        self.modification = datetime.datetime.now()
        self.version = 0
        self.children = []

    def print_node(self):
        print(self.name)
        print(self.data,"\n")
        aux = 0
        while(aux < len(self.children)):
           self.children[aux].print_node()
           aux += 1
        return

    def add_child(self, child):
        self.children.append(child)
        self.modification = datetime.datetime.now()
        self.version += 1
        return

    def add_data(self, data):
        self.data = data
        self.modification = datetime.datetime.now()
        self.version += 1
        return

    def delete_child(self, child):
        self.children.remove(child)
        self.modification = datetime.datetime.now()
        self.version += 1

    def search_name(self, name):
        aux = 0
        while(aux < len(self.children)):
            if(self.children[aux].name == name):
                return self.children[aux]
            aux += 1;
        return None

    def alter_data(self, data):
        self.data = data
        self.modification = datetime.datetime.now()
        self.version += 1
        return None

    def get_children(self, node, returnList):
        for child in node.children:
            returnList.append(child.name)
            child.get_children(child, returnList)

        return returnList
