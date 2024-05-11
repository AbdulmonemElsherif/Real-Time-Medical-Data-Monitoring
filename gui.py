import tkinter as tk
from tkinter import messagebox
import json
import redis
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Connect to Redis
redis_client = redis.Redis(host='redis-11813.c281.us-east-1-2.ec2.redns.redis-cloud.com', port=11813, password='SqT9hamM5W7MPQRmFxnUEe8cBauteWJy', db=0)

def plot_vital_signs(patient_id, canvas, ax1, ax2, filter_type=None):
    try:
        data = redis_client.get(patient_id)
        if data:
            vital_signs_list = json.loads(data)

            # Extract heart rate and blood pressure data
            heart_rates = [vs['heart_rate'] for vs in vital_signs_list]
            blood_pressures = [vs['blood_pressure'] for vs in vital_signs_list]

            # Clear previous plots
            ax1.clear()
            ax2.clear()

            # Plot heart rate
            if filter_type is None or filter_type == 'heart_rate':
                ax1.plot(heart_rates, label='Heart Rate', marker='o', color='red')
                ax1.set_title('Heart Rate')
                ax1.set_ylabel('BPM')
                ax1.legend()
                ax1.grid(True)

            # Plot blood pressure
            if filter_type is None or filter_type == 'blood_pressure':
                ax2.plot(blood_pressures, label='Blood Pressure', marker='o', color='blue')
                ax2.set_title('Blood Pressure')
                ax2.set_ylabel('mmHg')
                ax2.legend()
                ax2.grid(True)

            # Redraw plots in Tkinter window
            canvas.draw()
        else:
            messagebox.showinfo("Error", "Patient ID not found in database")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_vital_signs(patient_id, canvas, ax1, ax2, filter_type=None):
    plot_vital_signs(patient_id, canvas, ax1, ax2, filter_type)
    # Schedule the next update
    root.after(5000, update_vital_signs, patient_id, canvas, ax1, ax2, filter_type)

# Create Tkinter window
root = tk.Tk()
root.title("Real-Time Medical Data Monitoring")

# Search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Enter Patient ID:").pack(side=tk.LEFT)
patient_id_entry = tk.Entry(search_frame)
patient_id_entry.pack(side=tk.LEFT)
search_button = tk.Button(search_frame, text="Search", command=lambda: update_vital_signs(patient_id_entry.get(), canvas, ax1, ax2))
search_button.pack(side=tk.LEFT)
# Bonus feature: Filter by vital sign type
filter_var = tk.StringVar(root)
filter_options = tk.OptionMenu(root, filter_var, "All", "Heart Rate", "Blood Pressure")
filter_options.pack()
def apply_filter():
    filter_type = filter_var.get().lower().replace(" ", "_")
    if filter_type == "all":
        filter_type = None
    update_vital_signs(patient_id_entry.get(), canvas, ax1, ax2, filter_type)

filter_button = tk.Button(root, text="Apply Filter", command=apply_filter)
filter_button.pack()

# Plot area
fig = Figure(figsize=(12, 6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Run Tkinter event loop
root.mainloop()
