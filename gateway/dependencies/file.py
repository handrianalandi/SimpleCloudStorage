from nameko.rpc import rpc
import gateway.dependencies.database as database

class FileService:
    name = "file_service"

    database=database.Database()

    @rpc
    def upload_file(self, filename,filepath,user_id):
        # file.save(filepath)
        print("upload success")
        #save file to database
        return self.database.upload_file(filename, filepath, user_id)
        # return self.database.upload_file(file,filename,filepath,username)

    @rpc
    def get_file_list(self, user_id):
        return self.database.get_file_list(user_id)

    @rpc
    def share_file(self,file_id,user_origin,user_destination):
        return self.database.share_file(file_id,user_origin,user_destination)

    @rpc
    def get_shared_file_list(self,user_id):
        return self.database.get_shared_file_list(user_id)

    @rpc
    def download_file(self,file_id,user_id):
        return self.database.download_file(file_id,user_id)