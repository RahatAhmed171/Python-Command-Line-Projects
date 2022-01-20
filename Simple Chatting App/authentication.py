

import sqlite3
import hashlib

class UserAlreadyExists(Exception):
    #def __init__(self,username) -> None:
        #super().__init__(f'Account with username "{username}" already exists. Try again ')
    pass
class InvalidUserInfo(Exception):
    #def __init__(self) -> None:
        #super().__init__("Login Error. Invalid username or password. Try again")
    pass

class authentication_system:
    def __init__(self) -> None:
        self.user_info_storage=database_system()
        self.login_status=False
    
    def register_user(self,new_user_name,new_user_password):
        
        user_already_exists=self.user_info_storage.check_duplicate_user(new_user_name)
        if user_already_exists:
            raise UserAlreadyExists(new_user_name)
            
        else:
            encrypted_password=self._encrypt_pwd(new_user_name,new_user_password)
            self.user_info_storage.create_a_user(new_user_name,encrypted_password)
    
    def login_user(self,username,password):
       
        encrypted_password=self._encrypt_pwd(username,password)
        login_successful=self.user_info_storage.check_if_a_user_match(username,encrypted_password)
        if login_successful:
            return True
        else:
            raise InvalidUserInfo()

    def logout_user(self):
        self.login_status=False
        
            
            



    def _encrypt_pwd(self,username,password):
 
        hash_string = (username + password)
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

class database_system:
    def __init__(self):
        self.conn=sqlite3.connect("users.db")
        self.cursor_command=self.conn.cursor()
        self.check_if_table_exist()

    def create_a_table(self):
       self.cursor_command.execute('''CREATE TABLE USERS
                                  (
                                    username text,
                                    password text
                                    
                                  ) ''')


    def check_if_table_exist(self):
        result = self.cursor_command.execute("""SELECT name FROM sqlite_master WHERE type='table'AND name='USERS'; """).fetchall()
        if result==[]:
            self.create_a_table()
        else:
            return


    def create_a_user(self,name,password):
        
        with self.conn:
            self.cursor_command.execute("INSERT INTO USERS VALUES (:username,:password)",{'username':name,'password':password})
            print("success")

    def check_if_a_user_match(self,name,password):
        self.cursor_command.execute("SELECT * FROM USERS WHERE username= ? and password= ?",(name, password))
        found = self.cursor_command.fetchone()
        if found:
            return True
        else:
            return False

    
    def check_duplicate_user(self,name):
        self.cursor_command.execute("SELECT * FROM USERS WHERE username=?",(name,))
        found=self.cursor_command.fetchone()
        if found:
            return True
        else:
            return False
            






        
