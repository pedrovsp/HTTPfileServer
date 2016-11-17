
typedef string datetime

struct Node
{
    1:string name,
    2:string data,
    3:datetime creation,
    4:datetime modification,
    5:i32 version = 0,
    6:list<Node> children,
}

service SharedService
{
    list<string> get_children(1:Node node, 2:list<string> returnList),
    Node alter_data(1:Node node, 2:string data),
    Node search_name(1:Node node, 2:string name),
    Node delete_child(1:Node node, 2:Node child),
    Node add_data(1:Node node, 2:string data),
    Node add_child(1:Node node, 2:Node child),
    Node NodeInit(1:string name, 2:string data)
}
