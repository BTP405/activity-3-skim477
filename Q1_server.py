#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.


#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.

import socket
import pickle
import os

def run_server(save_directory):
    server_socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 12345)
    server_socket.bind(server_address)
    server_socket.listen(1)
    
    print("Server is listening for incoming connections...")
    
    while True:
        #Wait for a connection
        client_socket, client_address = server_socket.accept()
        print("Connect to: ", client_address)
        
        try:        
            #Receive data from the client
            data = client_socket.recv(1024)

            file_object = pickle.loads(data)
            file_path = os.path.join(save_directory, file_object['filename'])
            with open(file_path, 'wb') as file:
                file.write(file_object['file_data'])
            print(f"Received: {file_object['filename']}")

            #Send an acknowledgment back to the client
            message = "Message received by the server!"
            client_socket.sendall(message.encode())
        
        except (pickle.UnpicklingError, EOFError) as e:
            print(f"Error during file reception or saving: {e}")
            
        finally:
            #Clean up the connection
            client_socket.close()

if __name__ == "__main__":
    save_dir = 'c:/Users/SEONGJUN KIM/Desktop/BSD/6th Semester/BTP405/activity3/file/'
    run_server(save_dir)