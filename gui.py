import tkinter as tk
import subprocess
from tkinter import *
import board
import adafruit_dht
import time
import mpu6050

def show_content(page):
    global temperature_value, humidity_value, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
    # Clear previous content


    if page == "Home":
        # Configure grid for home page
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Home welcome message centered in the grid
        Label(content_frame, text="🏡 Welcome to the Home Page!", 
              font=("Arial", 18, "bold"), fg="black", bg="white").grid(row=0, column=0, padx=330, pady=196)

    elif page == "Reading":
        for i in range(3):  
            content_frame.columnconfigure(i, weight=0)
        for i in range(4):  
            content_frame.rowconfigure(i, weight=0)
        # Configure the content frame
        content_frame.configure(width=1024, height=462)
        content_frame.grid_propagate(False)  # Prevent resizing
        
        # Configure grid layout for content frame
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=0)  # Title row
        content_frame.rowconfigure(1, weight=1)  # Sensor content row
        
        # Title section
        title_frame = Frame(content_frame, bg="white")
        title_frame.grid(row=0, column=0, sticky="ew")
        
        # Configure grid for title frame
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        
        # Add title
        Label(title_frame, text="📡 Live Sensor Readings", 
              font=("Arial", 18, "bold"), fg="black", bg="white").grid(row=0, column=0, pady=10)

        # Main content container for sensors
        reading_container = Frame(content_frame, bg="white", height=412)
        reading_container.grid(row=1, column=0, sticky="nsew")
        reading_container.grid_propagate(False)
        
        # Configure grid for the reading container - two equal columns
        reading_container.columnconfigure(0, weight=1)  # Left sensor column
        reading_container.columnconfigure(1, weight=1)  # Right sensor column
        reading_container.rowconfigure(0, weight=1)     # Full height
        
        # Left side - DHT22 Sensor
        dht22_frame = Frame(reading_container, bg="#e0f7fa")
        dht22_frame.grid(row=0, column=0, sticky="nsew")
        dht22_frame.grid_propagate(False)
        
        # Configure grid for DHT22 frame
        dht22_frame.columnconfigure(0, weight=1)  # Center column
        dht22_frame.rowconfigure(0, weight=0)     # Title row
        dht22_frame.rowconfigure(1, weight=1)     # Content row
        
        # DHT22 Title
        Label(dht22_frame, text="🌡️ DHT22 Sensor", 
              font=("Arial", 16, "bold"), fg="black", bg="#e0f7fa").grid(row=0, column=0, pady=20)

        # DHT22 content frame
        dht_content = Frame(dht22_frame, bg="#e0f7fa")
        dht_content.grid(row=1, column=0)
        
        # Configure grid for DHT content
        dht_content.columnconfigure(0, weight=1)
        for i in range(4):  # 4 rows for temperature and humidity labels and values
            dht_content.rowconfigure(i, weight=1)

        # Temperature and Humidity display
        temperature_label = Label(content_frame, text="Temperature:", font=("Arial", 16, "bold"),  bg="#e0f7fa")
        temperature_value = Label(content_frame, text="--°C", font=("Arial", 24), bg="#e0f7fa")
        temperature_label.grid(row=0, column=0, pady=(20, 0))
        temperature_value.grid(row=1, column=0, pady=(5, 20))

        humidity_label = Label(content_frame, text="Humidity:", font=("Arial", 16, "bold"),bg="#e0f7fa")
        humidity_value = Label(content_frame, text="--%", font=("Arial", 24), bg="#e0f7fa")
        humidity_label.grid(row=2, column=0, pady=(20, 0))
        humidity_value.grid(row=3, column=0, pady=(5, 20))

        # Start updating sensor readings
        update_DHT_sensor_readings()

        # Right side - Motion Sensor
        motion_frame = Frame(reading_container, bg="#fce4ec")
        motion_frame.grid(row=0, column=1, sticky="nsew")
        motion_frame.grid_propagate(False)
        
        # Configure grid for motion frame
        motion_frame.columnconfigure(0, weight=1)  # Center column
        motion_frame.rowconfigure(0, weight=0)     # Title row
        motion_frame.rowconfigure(1, weight=1)     # Content row
        
        # Motion sensor title
        Label(motion_frame, text="🔄 Motion Sensor (MPU6050)", 
              font=("Arial", 16, "bold"), fg="black", bg="#fce4ec").grid(row=0, column=0, pady=20)

        # Motion content frame
        motion_content = Frame(motion_frame, bg="#fce4ec")
        motion_content.grid(row=1, column=0)
        
        # Configure grid for motion content - two columns for accel and gyro
        motion_content.columnconfigure(0, weight=1)  # Accel column
        motion_content.columnconfigure(1, weight=1)  # Gyro column
        motion_content.rowconfigure(0, weight=1)     # Full height
        
        # Acceleration column
        accel_frame = Frame(motion_content, bg="#fce4ec")
        accel_frame.grid(row=0, column=0, padx=30)
        
        # Configure grid for acceleration frame
        accel_frame.columnconfigure(0, weight=1)
        for i in range(4):  # 4 rows: title and 3 values
            accel_frame.rowconfigure(i, weight=1)
        
        # Acceleration title and values
        Label(accel_frame, text="Acceleration:", 
             font=("Arial", 16, "bold"), bg="#fce4ec").grid(row=0, column=0, pady=(0, 10))
        
        accel_x = Label(accel_frame, text="X: --", font=("Arial", 14), bg="#fce4ec")
        accel_y = Label(accel_frame, text="Y: --", font=("Arial", 14), bg="#fce4ec")
        accel_z = Label(accel_frame, text="Z: --", font=("Arial", 14), bg="#fce4ec")
        
        accel_x.grid(row=1, column=0, pady=5)
        accel_y.grid(row=2, column=0, pady=5)
        accel_z.grid(row=3, column=0, pady=5)
        
        # Gyroscope column
        gyro_frame = Frame(motion_content, bg="#fce4ec")
        gyro_frame.grid(row=0, column=1, padx=30)
        
        # Configure grid for gyroscope frame
        gyro_frame.columnconfigure(0, weight=1)
        for i in range(4):  # 4 rows: title and 3 values
            gyro_frame.rowconfigure(i, weight=1)
        
        # Gyroscope title and values
        Label(gyro_frame, text="Gyroscope:", 
             font=("Arial", 16, "bold"), bg="#fce4ec").grid(row=0, column=0, pady=(0, 10))
        
        gyro_x = Label(gyro_frame, text="X: --", font=("Arial", 14), bg="#fce4ec")
        gyro_y = Label(gyro_frame, text="Y: --", font=("Arial", 14), bg="#fce4ec")
        gyro_z = Label(gyro_frame, text="Z: --", font=("Arial", 14), bg="#fce4ec")
        
        gyro_x.grid(row=1, column=0, pady=5)
        gyro_y.grid(row=2, column=0, pady=5)
        gyro_z.grid(row=3, column=0, pady=5)

        # Start updating sensor readings
        update_motion_sensor_readings()

    elif page == "Debug":
        for i in range(3):  
            content_frame.columnconfigure(i, weight=0)
        for i in range(4):  
            content_frame.rowconfigure(i, weight=0)
          # Configure content frame with fixed dimensions
        content_frame.configure(width=1024, height=462)
        content_frame.grid_propagate(False)  # Prevent resizing
        
        content_frame.columnconfigure(0, weight=1) 
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=0)  # Title row
        content_frame.rowconfigure(1, weight=1)  # Sensor content row
        content_frame.rowconfigure(2, weight=1)     # Bottom buttons row
        content_frame.rowconfigure(3, weight=1)     # Middle button row
        # Debug title
        Label(content_frame, text="🔧 Debug Mode", 
            font=("Arial", 18, "bold"), fg="black").grid(row=0, column=0, columnspan=2, pady=20)

        # Create a consistent style for all debug buttons
        button_style = {
            "bg": "#007acc",
            "fg": "white",
            "font": ("Arial", 14, "bold"),
            "padx": 20,
            "pady": 15,
            "width": 15  # Fixed width for uniform appearance
        }
        
        # Top left - Debug LED button
        debug_led_button = Button(content_frame, text="Debug LED", command=lambda: run_debug("led"), **button_style)
        debug_led_button.grid(row=1, column=0, padx=30, pady=30, sticky="nsew")
        
        # Top right - Debug Button
        debug_button_button = Button(content_frame, text="Debug Button", command=lambda: run_debug("button"), **button_style)
        debug_button_button.grid(row=1, column=1, padx=30, pady=30, sticky="nsew")
        
        # Bottom left - Debug DHT22
        debug_dht22_button = Button(content_frame, text="Debug DHT22", command=lambda: run_debug("dht22"), **button_style)
        debug_dht22_button.grid(row=2, column=0, padx=30, pady=30, sticky="nsew")
        
        # Bottom right - Debug Motion Sensor
        debug_motion_button = Button(content_frame, text="Debug Motion", command=lambda: run_debug("motion"), **button_style)
        debug_motion_button.grid(row=2, column=1, padx=30, pady=30, sticky="nsew")
        
        # Middle button - Run all debug tests
        all_debug_button = Button(content_frame, text="Run All Debug Tests", 
                            command=lambda: run_debug("all"), 
                            bg="#007acc", 
                            fg="white", 
                            font=("Arial", 16, "bold"),
                            padx=20, 
                            pady=10,
                            width=20)
        all_debug_button.grid(row=3, column=0, columnspan=2, pady=30)

def run_debug():
    subprocess.run(['python3', 'debug.py'])

# Function to update sensor readings
def update_DHT_sensor_readings():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        
        if temperature is not None and humidity is not None:
            temperature_value.config(text=f"{temperature:.1f}°C")
            humidity_value.config(text=f"{humidity:.1f}%")
        else:
            temperature_value.config(text="Error")
            humidity_value.config(text="Error")

    except RuntimeError as error:
        print(f"Reading error: {error}")
        temperature_value.config(text="Retrying...")
        humidity_value.config(text="Retrying...")

    except Exception as error:
        print(f"Sensor failure: {error}")
        dhtDevice.exit()

    # Schedule next update every 1 seconds
    content_frame.after(1000, update_DHT_sensor_readings)

# Function to Update Sensor Readings
def update_motion_sensor_readings():
    try:
        accelerometer_data = mpu6050.get_accel_data()
        gyro_data = mpu6050.get_gyro_data()
        
        # Update Acceleration Labels
        accel_x.config(text=f"X: {accelerometer_data['x']:.2f}")
        accel_y.config(text=f"Y: {accelerometer_data['y']:.2f}")
        accel_z.config(text=f"Z: {accelerometer_data['z']:.2f}")

        # Update Gyroscope Labels
        gyro_x.config(text=f"X: {gyro_data['x']:.2f}")
        gyro_y.config(text=f"Y: {gyro_data['y']:.2f}")
        gyro_z.config(text=f"Z: {gyro_data['z']:.2f}")

    except Exception as e:
        print(f"Error reading sensor: {e}")

    # Call function again after 1 second
    content_frame.after(1000, update_motion_sensor_readings)

#Configuration 
dhtDevice = adafruit_dht.DHT22(board.D18)
mpu6050 = mpu6050.mpu6050(0x68) #0x68 is the i2c address

# Main Window
window = Tk()
window.title("Kai Sheng's Mini Project")
window.geometry('1024x512')
window.resizable(False, False)  
window.configure(bg="#f0f0f0")
window.columnconfigure(0, weight=1)  # Configure grid for window
window.rowconfigure(0, weight=0)     # Nav bar row
window.rowconfigure(1, weight=1)     # Content row

# Navigation Bar
nav_frame = Frame(window, bg="#007acc", height=50)
nav_frame.grid(row=0, column=0, sticky="ew")

# Configure grid for nav frame - three columns for buttons
nav_frame.columnconfigure(0, weight=0)  # Home button
nav_frame.columnconfigure(1, weight=0)  # Reading button
nav_frame.columnconfigure(2, weight=0)  # Debug button
nav_frame.columnconfigure(3, weight=1)  # Empty space
nav_frame.rowconfigure(0, weight=1)     # Single row

# Navigation Buttons
Button(nav_frame, text="🏡 Home", font=("Arial", 14, "bold"), bg="#005a9e", fg="white",
       padx=30, pady=10, command=lambda: show_content("Home")).grid(row=0, column=0)

Button(nav_frame, text="📡 Reading", font=("Arial", 14, "bold"), bg="#005a9e", fg="white",
       padx=30, pady=10, command=lambda: show_content("Reading")).grid(row=0, column=1, padx=50)

Button(nav_frame, text="🔧 Debug", font=("Arial", 14, "bold"), bg="#005a9e", fg="white",
       padx=30, pady=10, command=lambda: show_content("Debug")).grid(row=0, column=2)

# Main content area
main_frame = Frame(window, bg="white")
main_frame.grid(row=1, column=0, sticky="nsew")

# Configure grid for main frame
main_frame.columnconfigure(0, weight=1)  # Canvas column
main_frame.columnconfigure(1, weight=0)  # Scrollbar column
main_frame.rowconfigure(0, weight=1)     # Single row

# Canvas and scrollbar
canvas = Canvas(main_frame, bg="white")
scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)

# Configure canvas
canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = Frame(canvas, bg="white")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
window_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Position canvas and scrollbar with grid
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Configure grid for scrollable frame
scrollable_frame.columnconfigure(0, weight=1)
scrollable_frame.rowconfigure(0, weight=1)

# Content frame inside Scrollable Frame
content_frame = Frame(scrollable_frame, bg="white")
content_frame.grid(row=0, column=0, sticky="nsew")


# Load Home Page by default
show_content("Home")

# Run GUI
window.mainloop()