from nameko.rpc import rpc
import gateway.dependencies.database as database

class UserService:

    name = "user_service"

    database=database.Database()

    @rpc
    def login(self, username, password):
        exist,user= self.database.login(username, password)
        if exist:
            return True,user
        return False,user

    
    @rpc
    def register(self, username, password):
        exist,user= self.database.login(username, password)
        if exist:
            return False,user
        success=self.database.register(username, password)
        if success:
            return True,username
        return False,username

    @rpc
    def get_user_id(self, username):
        return self.database.get_user_id(username)
