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
    oxygen_saturation = random.randint(95, 100)  # Normal range is 95-100%
    body_temperature = random.uniform(36.5, 37.5)  # Normal range is 36.5-37.5°C
    return {'heart_rate': heart_rate, 'blood_pressure': blood_pressure, 'oxygen_saturation': oxygen_saturation, 'body_temperature': body_temperature}
def send_data(patient_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_ADDRESS, SERVER_PORT))
        while True:
            try:
                vital_signs = generate_vital_signs()
                data = {'patient_id': patient_id, 'vital_signs': vital_signs}
                serialized_data = json.dumps(data)
                s.sendall(serialized_data.encode())
                print("Data sent:", serialized_data)
                time.sleep(5)  # Send data every 5 seconds
            except ConnectionResetError:
                print("Connection was closed by the server.")
                break

if __name__ == "__main__":
    patient_id = 1  # Replace with the desired patient ID
    send_data(patient_id)