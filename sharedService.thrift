
typedef string Timestamp

struct Node
{
    1:string name,
    2:string data,
    3:Timestamp creation,
    4:Timestamp modification,
    5:i32 version = 0,
    6:list<Node> children
}

service SharedService
{
    Node getNode(1: string path)
}
