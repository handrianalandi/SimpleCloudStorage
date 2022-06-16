import datetime
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
import uuid
import json

from gateway.dependencies.session import SessionProvider

class User:
    def __init__(self, name, password):
        self.username = name
        self.password = password
    
    #print
    def __str__(self):
        return 'User: {}, Password: {}'.format(self.username, self.password)


class Service:
    name = "gateway_service"

    user_rpc=RpcProxy('user_service')
    file_rpc=RpcProxy('file_service')
    session_provider = SessionProvider()

    
    @http('POST', '/login')
    def login(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            session_data = self.session_provider.get_session(session_id)
            #get username
            username = session_data.get("username")
            return Response(f"You are already logged in as {username}")
        else:
            #check if username and password is exist in the body
            username = request.get_json()['username']
            password = request.get_json()['password']
            exist,user= self.user_rpc.login(username, password)
            #check if user exists
            if exist:
                user_data = {
                    'username': username
                }
                session_id = self.session_provider.set_session(user_data)
                response = Response(f"Welcome {username}")
                response.set_cookie('SESSID', session_id)
                return response
            else:
                return Response("Please check your username and password!")


    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            response = Response(self.session_provider.delete_session(cookies['SESSID']))
            response.set_cookie('SESSID', '', expires=0)
            return response
        else:
            response = Response('You need to Login First')
            return response

    @http('POST', '/register')
    def register(self, request):
        username = request.get_json()['username']
        password = request.get_json()['password']
        success,username= self.user_rpc.register(username, password)
        if(success):
            user_data={
                'username': username,
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response("Register Success!, Welcome {}".format(username))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            return Response("Register Failed, Username already exist!")

    @http('POST', '/upload')
    def upload_file(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            session_data = self.session_provider.get_session(session_id)
            # print(session_data['username'])
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            file = request.files['file']
            filename = file.filename
            print(filename)
            file_type=filename.split('.')[-1]
            filename=filename.split('.')[0]
            today = str(datetime.datetime.now())
            #remove miliseconds
            today=today.split('.')[0]
            today=today.replace(':','')
            filepath = 'file/{}{}.{}'.format(filename, today,file_type)
            #remove spaces
            if(self.file_rpc.upload_file(file.filename,filepath,user_id)):
                file.save(filepath)
                return Response("Upload Success!")
            else:
                return Response("Upload Failed!")
        else:
            return Response("You need to Login First")

    @http('GET', '/files')
    def get_files(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            session_data = self.session_provider.get_session(session_id)
            # print(session_data['username'])
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            files=self.file_rpc.get_file_list(user_id)
            #create json that consist of array your file
            your_files=[]
            for file in files:
                your_files.append(file.get('name'))

            shared_files=self.file_rpc.get_shared_file_list(user_id)
            shared_files_json=[]
            for file in shared_files:
                shared_files_json.append(file.get('name'))


            result={
                'your_files':your_files,
                'shared_files':shared_files_json
            }
            return Response(json.dumps(result))
        else:
            return Response("You need to Login First")

    @http('POST', '/share')
    def share_file(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            session_data = self.session_provider.get_session(session_id)
            # print(session_data['username'])
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            file_id=request.get_json()['file_id']
            user_destination=request.get_json()['user_destination_id']
            success,message=self.file_rpc.share_file(file_id,user_id,user_destination)
            return Response(message)
        else:
            return Response("You need to Login First")

    @http('POST', '/download')
    def download_file(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            session_data = self.session_provider.get_session(session_id)
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            file_id=request.get_json()['file_id']
            success,file_path,filename=self.file_rpc.download_file(file_id,user_id)
            if(success):
                response = Response(open(file_path, 'rb').read())
                #get file type
                file_type=filename.split('.')[-1]
                if(file_type=='jpg' or file_type=='png' or file_type=='jpeg' or file_type=='gif'):
                    if file_type=='jpg':
                        file_type='jpeg'
                    response.headers['Content-Type'] = 'image/{}'.format(file_type)
                else:
                    response.headers['Content-Type'] = 'application/{}'.format(file_type)
                #replace spaces with underscore
                filename=filename.replace(' ','_')
                response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
                return response
            else:
                return Response(file_path)
        else:
            return Response("You need to Login First")



            
    
    
    

