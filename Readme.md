# Real-Time Medical Data Monitoring

This project is a simple GUI application for real-time monitoring of medical data. It retrieves patient data from a Redis database and displays it in a graphical format. The GUI has been updated to a dark theme for better visibility and user experience.

## Features

- Search for patient data using a patient ID
- Real-time monitoring of heart rate, blood pressure, oxygen saturation, and body temperature
- Filter data by vital sign type
- Display patient data in a tabular format

## How to Run

1. Install the required Python packages:

    `pip install redis matplotlib tkinter`
    
2. Run the application:

    `python gui.py`
    
3. Enter a patient ID in the search bar and click "Search" to retrieve and display the patient's data.
4. Use the filter option to filter the data by vital sign type.