include "sharedService.thrift"

service RequestHandler extends sharedService.SharedService
{
    string do_post(1:string message, 2:string path)
    string do_update(1:string body, 2:string path)
    string do_update_version(1:string body, 2:i32 version, 3:string path)
    string do_delete_version(1:i32 version, 2:string path)
    string do_list(1:string path)
    string do_delete(1:string path)
    string do_get(1:string path)
}
