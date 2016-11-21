
typedef string datetime

struct Counter
{
    1:i32 counter = 0
}

struct ServerCounter
{
    1:i32 counter = 0
}

struct PortList
{
    1:list<i32> ports
}

struct Node
{
    1:string name;
    2:string data;
    3:datetime creation;
    4:datetime modification;
    5:i32 version = 0;
    6:i32 id = 0;
    7:list<i32> children
}

struct NodeList
{
    1:list<Node> lista
}

service SharedService
{
    list<string> get_children(1:Node node, 2:list<string> returnList),
    Node alter_data(1:Node node, 2:string data),
    Node search_name(1:Node node, 2:string name),
    Node delete_child(1:Node node, 2:Node child),
    Node add_data(1:Node node, 2:string data),
    Node add_child(1:Node node, 2:Node child),
    void incrementCounter(),
    void incrementServerCounter(),
    i32  getServerCount(),
    NodeList getNodeList(),
    i32  getCounter(),
    void setServerCount(1:i32 r_count),
    void setNodeList(1:list<Node> lista),
    void setCounter(1:i32 r_count),
    void addPort(1:i32 porta),
}