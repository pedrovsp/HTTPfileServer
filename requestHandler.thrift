include "sharedService.thrift"

service RequestHandler extends sharedService.SharedService
{
    string do_update(1:string data, 2:string path, 3:sharedService.Node current_node)
    string do_get(1:string path)
    string do_add(1:string data, 2:string path, 3:sharedService.Node current_node)
    string do_update_version(1:string body, 2:i32 version, 3:string path, 4:sharedService.Node current_node)
    string do_delete(1:string path)
    string do_delete_version(1:string path, 2:i32 version)
    string do_list(1:string path)
}
