import socket
import pickle
import os

    
def run_client(file_path):

    server_address = ('127.0.0.1', 12345)

    
    try:
        with open(file_path, 'rb') as file:
            file_object = {
                'filename': os.path.basename(file_path),
                'file_data': file.read()
            }
            pickled_object = pickle.dumps(file_object)      
            
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              
        client_socket.connect(server_address)
        client_socket.sendall(pickled_object)
        
    except IOError as e:
        print(f"IO Error: {e}")
        
    # except socket.error as e:
    #     print(f"Socket error: {e}")
        
    except pickle.PicklingError as e:
        print(f"Pickling error: {e}")
        
        # #Receive the acknowledgment from the server
        # data = client_socket.recv(1024)
        # print("Received acknowledgment: ", data.decode())
    
    finally:
        #Clean up the connection
        client_socket.close()
        
if __name__ == "__main__":
    file_path = 'c:/Users/SEONGJUN KIM/Desktop/BSD/6th Semester/BTP405/activity3/filename.txt'
    
    run_client(file_path)
    #run_client()
    
