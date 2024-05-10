import json
import socket
import redis

# Define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Connect to Redis
redis_client = redis.Redis(host='redis-11813.c281.us-east-1-2.ec2.redns.redis-cloud.com', port=11813, password='SqT9hamM5W7MPQRmFxnUEe8cBauteWJy', db=0)

def handle_client_connection(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break
        decoded_data = data.decode()
        print("Data received:", decoded_data)

        # Parse received data
        try:
            parsed_data = json.loads(decoded_data)
            patient_id = parsed_data['patient_id']
            vital_signs = parsed_data['vital_signs']
            # Store data in Redis
            redis_client.set(patient_id, json.dumps(vital_signs))
        except json.JSONDecodeError:
            print("Error decoding JSON data")
        except KeyError:
            print("Missing key in JSON data")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
        server_socket.listen(5)
        print("Server is listening...")
        while True:
            client_socket, _ = server_socket.accept()
            print("New client connected")
            handle_client_connection(client_socket)

if __name__ == "__main__":
    start_server()
