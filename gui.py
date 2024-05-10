import tkinter as tk
from tkinter import messagebox
import json
import redis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Connect to Redis
redis_client = redis.Redis(host='redis-11813.c281.us-east-1-2.ec2.redns.redis-cloud.com', port=11813, password='SqT9hamM5W7MPQRmFxnUEe8cBauteWJy', db=0)

def plot_data(patient_id):
    try:
        data = redis_client.get(patient_id)
        if data:
            vital_signs = json.loads(data)
            heart_rate = vital_signs.get('heart_rate', [])
            blood_pressure = vital_signs.get('blood_pressure', [])

            # Plot data
            plt.figure(figsize=(6, 4))
            plt.plot(heart_rate, label='Heart Rate', marker='o')
            plt.plot(blood_pressure, label='Blood Pressure', marker='o')
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.title('Vital Signs Over Time')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            # Show plot in Tkinter window
            canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        else:
            messagebox.showinfo("Error", "Patient ID not found in database")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_patient():
    patient_id = patient_id_entry.get()
    plot_data(patient_id)

# Create Tkinter window
root = tk.Tk()
root.title("Real-Time Medical Data Monitoring")

# Search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Enter Patient ID:").pack(side=tk.LEFT)
patient_id_entry = tk.Entry(search_frame)
patient_id_entry.pack(side=tk.LEFT)
search_button = tk.Button(search_frame, text="Search", command=search_patient)
search_button.pack(side=tk.LEFT)

# Run Tkinter event loop
root.mainloop()
