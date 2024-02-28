import socket
import pickle
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(4096)
            if message:
                data = pickle.loads(message)
                print(f"New message: {data}")

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_messages(client_socket):
    while True:
        message = input("")
        try:
            serialized_message = pickle.dumps(message)
            client_socket.send(serialized_message )        
                
            if message.lower() == "disconnect":
                send_disconnect(client_socket)
                break

            
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def send_disconnect(client_socket):
     print("Disconnected")
     client_socket.close()


def main():
    server_address = ('127.0.0.1', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    print("Connected to the server.")
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    send_messages(client_socket)

if __name__ == "__main__":
    main()