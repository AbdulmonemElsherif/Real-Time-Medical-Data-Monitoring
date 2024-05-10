import json
import random
import socket
import time

# Define server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

def generate_vital_signs():
    # Simulate generating vital signs data
    heart_rate = random.randint(60, 100)
    blood_pressure = random.randint(80, 120)
    return {'heart_rate': heart_rate, 'blood_pressure': blood_pressure}

def send_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_ADDRESS, SERVER_PORT))
        while True:
            patient_id = random.randint(1, 100)
            vital_signs = generate_vital_signs()
            data = {'patient_id': patient_id, 'vital_signs': vital_signs}
            serialized_data = json.dumps(data)
            s.sendall(serialized_data.encode())
            print("Data sent:", serialized_data)
            time.sleep(5)  # Send data every 5 seconds

if __name__ == "__main__":
    send_data()
