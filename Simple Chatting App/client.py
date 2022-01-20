
import socket
import sys
import threading


class User:
    def __init__(self):
        self.port=5050
        self.message_coding='utf-8'
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.thread=None
        self.exited_from_chatroom=None

    def connect_to_server(self,server_address):
        
        self.client.connect((server_address,self.port))
        self.talking_to_server()
    
    
    def talking_to_server(self):
        send_a_message=''
        while True:
            count_of_thread=threading.activeCount()
            
            if count_of_thread==2:
                recieved_message=self.client.recv(1024).decode(self.message_coding)
                print(recieved_message)
                if self.exited_from_chatroom!=None:
                    exit()
            
            else:
                recieved_message=self.client.recv(1024).decode(self.message_coding)
                if recieved_message=='DISCONNECT':
                    break
                elif recieved_message=='logintrue':
                    self.start_a_thread()
                else:
                    send_a_message=input(f'{recieved_message}')
                    self.client.send(send_a_message.encode(self.message_coding))

            
                    
    
    def chatroom_message_prompt(self):
        send_a_message=''
        while True:
            send_a_message=input()
            if send_a_message=="DISCONNECT":
                self.client.send(send_a_message.encode(self.message_coding))
                self.exited_from_chatroom=True
                sys.exit()
                
            else:
                self.client.send(send_a_message.encode(self.message_coding))
        
    def start_a_thread(self):
         self.thread=threading.Thread(target=self.chatroom_message_prompt,args=())
         self.thread.start()
         
            
try:
    server_address=input(str("Enter the server address to connect to chat app:"))
    User().connect_to_server(server_address)
    
except ConnectionResetError:
    print('Server has terminated the connection with you')
except ConnectionRefusedError:
    print('Sorry server is down at the moment')
except Exception:
    print('Some error has occured. Please try again')

