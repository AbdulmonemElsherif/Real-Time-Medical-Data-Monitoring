import json
import socket
import threading
import redis

# Define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Connect to Redis
redis_client = redis.Redis(host='redis-11813.c281.us-east-1-2.ec2.redns.redis-cloud.com', port=11813, password='SqT9hamM5W7MPQRmFxnUEe8cBauteWJy', db=0)

MAX_DATA_POINTS = 20  # Maximum number of data points to store for each patient

def handle_client_connection(client_socket):
    while True:
        try:
            request = client_socket.recv(1024)
            if not request:
                break  # Client disconnected
            data = json.loads(request.decode())
            patient_id = data['patient_id']
            vital_signs = data['vital_signs']

            # Retrieve existing data for the patient
            existing_data = redis_client.get(patient_id)
            if existing_data:
                existing_data = json.loads(existing_data)
            else:
                existing_data = []

            # Ensure existing_data is a list
            if not isinstance(existing_data, list):
                print('Existing data is not a list:', existing_data)
                existing_data = []

            # Append new data and keep only the last MAX_DATA_POINTS
            existing_data.append(vital_signs)
            existing_data = existing_data[-MAX_DATA_POINTS:]

            # Store updated data in Redis
            redis_client.set(patient_id, json.dumps(existing_data))

            print('Received data:', data)
            client_socket.send('ACK'.encode())
        except Exception as e:
            print("Error handling client data:", e)
            break
    client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
        server_socket.listen(5)
        print("Server is listening...")
        while True:
            client_socket, _ = server_socket.accept()
            print("New client connected")
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    start_server()
