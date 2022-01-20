import sys
import authentication
import socket
import threading

class ChatServer:
    def __init__(self) -> None:
        self.port=5050
        self.message_coding='utf-8'
        self.host=socket.gethostbyname(socket.gethostname())
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        self.list_of_clients=[]
        
    def start_the_server(self):
        self.server.listen()
        print(f'Server is on {self.host}')
        self.accept_a_client()
    
    def handle_a_client(self,communication_socket,address):
        print(f'server connected to {address}')
        authenticator=self.get_authentication_instance()
        
        choices={
            '1': self.signup,
            '2': self.login,
        }

        try: 
            
            communication_socket.send('''Welcome to the Live Simple Chat App. 
            In order to enter the live chat room, you need to log in.
            Press 1 to signup
            Press 2 to login
            Press 3 to disconnect from the server'''
                .encode(self.message_coding))
        
            connected=True
            while connected:
                communication_socket.send('Enter the choice:'.encode(self.message_coding))
                incoming_message=communication_socket.recv(1024).decode(self.message_coding)
                if incoming_message:
                    if incoming_message=='3':
                    
                        break
                    else:
                        try:
                            func=choices[incoming_message]
                            func(communication_socket,authenticator)
                        except KeyError:
                            communication_socket.send("Invalid choice".encode(self.message_coding))
            self.send_a_disconnect_message(communication_socket)
            self.disconnect_a_client(communication_socket)
            sys.exit()

        except ConnectionResetError:
            print("A client has terminated connection with server forcibly")
        except Exception:
            print("Some other problem has occured")

        

    def login(self,communication_socket,authenticator):
        
        username,password=self.get_user_info(communication_socket)
        try:
            authenticator.login_user(username,password)
            communication_socket.send('logintrue'.encode(self.message_coding))
            
            self.chatroom(communication_socket,username)
        except authentication.InvalidUserInfo:
            communication_socket.send(f'Invalid username or password\n'.encode(self.message_coding))
    
    def signup(self,communication_socket,authenticator):
        
        username,password=self.get_user_info(communication_socket)
        try:
            authenticator.register_user(username,password)
        except authentication.UserAlreadyExists:
            communication_socket.send('This user already exists. Try again'.encode(self.message_coding))

    def get_user_info(self,communication_socket):
        communication_socket.send("Enter the username:".encode(self.message_coding))
        recieved_username=communication_socket.recv(1024).decode(self.message_coding)
        communication_socket.send("Enter the password:".encode(self.message_coding))
        recieved_password=communication_socket.recv(1024).decode(self.message_coding)
        return recieved_username,recieved_password



    def get_authentication_instance(self):
        authenticator=authentication.authentication_system()
        return authenticator


    def disconnect_a_client(self,client,username=None):
        print(f'Connection is terminated with {username}')
        
        
        client.close()
    
    def chatroom(self,communication_socket,username):
        self.list_of_clients.append(communication_socket)
        communication_socket.send('''Welcome to the chatroom. You can send message to other people.
To leave chatroom type "DISCONNECT". You'll be signed out automatically and disconnected 
from the server\n'''.encode(self.message_coding))
        while True:
            
            recieved_message=communication_socket.recv(1024).decode(self.message_coding)
            if recieved_message=="DISCONNECT":
                broadcast_message=f'{username} has left the chatroom'
                self.broadcast_a_message(broadcast_message)
                self.list_of_clients.remove(communication_socket)

               
                break
            else:
                broadcast_message=f'{username}: {recieved_message}'
                self.broadcast_a_message(broadcast_message)
        
        self.disconnect_a_client(communication_socket,username)
        sys.exit()
        
        
        
        

    def send_a_disconnect_message(self,client_to_be_send):
        client_to_be_send.send("DISCONNECT".encode(self.message_coding))   

    def broadcast_a_message(self,message):
        for clients in self.list_of_clients:
            clients.send(message.encode(self.message_coding))

        
    
    def accept_a_client(self):
        while True:
            
            communication_socket,address=self.server.accept()
            
            thread=threading.Thread(target=self.handle_a_client,args=(communication_socket,address))
            thread.start()
            print(threading.activeCount()-1)


ChatServer().start_the_server()




    
