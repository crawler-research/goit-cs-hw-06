import socket
from concurrent import futures as cf
import urllib.parse
from datetime import datetime

TCP_IP = "localhost"
TCP_PORT = 5006

# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["MaksymDB"]
# collection = db["messages"]

def create_message(username, message, date):
    message = {"username": username, "message": message, "date": date}
    cat = {"name": name, "age": age, "features": features}
    collection.insert_one(cat)


def run_server(ip, port):
    def handle(sock: socket.socket, address: str):
        print(f"Connection established {address}")
        while True:
            received = sock.recv(10048)
            if not received:
                break
            # parse data
            data_dict = {key: value for key, value in [el.split('=') for el in urllib.parse.unquote_plus(received.decode()).split('&')]}

            # add date
            data_dict['date'] = datetime.now().isoformat()

            print("Writing to MongoDB:", data_dict)

            # create_message(data_dict['username'], data_dict['message'], data_dict['date'])

            sock.send('200'.encode())
        print(f"Socket connection closed {address}")
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    print(f"Start echo server {server_socket.getsockname()}")
    with cf.ThreadPoolExecutor(10) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f"Destroy server")
        finally:
            server_socket.close()


if __name__ == "__main__":
    run_server(TCP_IP, TCP_PORT)
