from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM user WHERE username = '{}' AND password = '{}'".format(username, password)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        #check if user exist
        if result is None:
            return False,result
        return True,result

    def register(self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        #check if user exist
        sql = "SELECT * FROM user WHERE username = '{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is not None:
            return False
        sql = "INSERT INTO user (username, password) VALUES ('{}', '{}')".format(username, password)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return True

    def get_user_id(self, username):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT id FROM user WHERE username = '{}'".format(username)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result['id']

    def upload_file(self, filename, filepath, user_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO file (id_user, name, location) VALUES ('{}', '{}', '{}')".format(user_id, filename, filepath)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        #check if file upload success
        if cursor.lastrowid is None:
            return False
        return True

    def get_file_list(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM file WHERE id_user = '{}'".format(user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def share_file(self, file_id, user_origin, user_destination):
        cursor = self.connection.cursor(dictionary=True)

        #check if file belong to user_origin
        sql = "SELECT * FROM file WHERE id = '{}' AND id_user = '{}'".format(file_id, user_origin)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            return False,"File not belong to user_origin"
        #check if user_destination exist
        sql = "SELECT * FROM user WHERE id = '{}'".format(user_destination)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            return False,"User_destination not exist"
        #share file
        sql = "INSERT INTO share (id_file, id_user_origin, id_user_destination) VALUES ('{}', '{}', '{}')".format(file_id, user_origin, user_destination)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        #check if file share success
        if cursor.lastrowid is None:
            return False,"File not share"
        return True,"File share success"

    def get_shared_file_list(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM file WHERE id IN (SELECT id_file FROM share WHERE id_user_destination = '{}')".format(user_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def download_file(self, file_id, user_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM file WHERE id = '{}' AND id_user = '{}'".format(file_id, user_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return False,"File not belong to user","noname"
        return True,result['location'],result['name']


    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='simplecloud',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
