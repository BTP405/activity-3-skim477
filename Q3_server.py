#Real-Time Chat Application with Pickling:

#Develop a simple real-time chat application where multiple clients can communicate with each other via a central server using sockets. 
#Messages sent by clients should be pickled before transmission. The server should receive pickled messages, unpickle them, and broadcast them to all connected clients.


#Requirements:
#Implement separate threads for handling client connections and message broadcasting on the server side.
#Ensure proper synchronization to handle concurrent access to shared resources (e.g., the list of connected clients).
#Allow clients to join and leave the chat room dynamically while maintaining active connections with other clients.
#Use pickling to serialize and deserialize messages exchanged between clients and the server.

import socket
import threading

class ChatServer:
    def __init__(self):
        server_address = ('127.0.0.1', 12345)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(server_address)
        self.server_socket.listen()

    def broadcast(self, message, source_client):
        with self.clients_lock:
            for client in self.clients:
                if client != source_client:
                    try:
                        client.send(message)
                            
                    except Exception as e:
                        print(f"Error sending message to client: {e}")
                        self.clients.remove(client)

    def handle_client(self, client_socket):
        connected = True
        while connected:
            try:
                message = client_socket.recv(4096)
                if message:
                    self.broadcast(message, client_socket)
                    
                    # if message == "disconnect":
                    #     connected = False
                    #     print("disconnected")
                       
                else:
                    break
            except Exception:
                break
        
        print("Client disconnected")
        with self.clients_lock:
            self.clients.remove(client_socket)
            
        client_socket.close()

    def start(self):
        print("Server is listening for incoming connections...")
        
        while True:
            client_socket, _ = self.server_socket.accept()
            with self.clients_lock:
                self.clients.append(client_socket)
                
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()