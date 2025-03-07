import tkinter as tk
import subprocess
from tkinter import *
import board
import adafruit_dht
import time
import mpu6050
from tkinter import messagebox
import RPi.GPIO as GPIO
import webbrowser
def show_content(page):
    global temperature_value, humidity_value, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
    # Clear previous content

    if page == "Home":
        # Clear any existing column and row configurations
        for i in range(3):  
            content_frame.columnconfigure(i, weight=0)
        for i in range(4):  
            content_frame.rowconfigure(i, weight=0)
        
        # Set fixed dimensions
        content_frame.configure(width=1024, height=512)
        content_frame.grid_propagate(False)  # Prevent resizing
        
        # Configure grid for home page - one column, two rows
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)  # Row for welcome message
        content_frame.rowconfigure(1, weight=0)  # Row for hyperlink
        
        # Create a container frame for better centering
        center_frame = tk.Frame(content_frame, bg="white")
        center_frame.grid(row=0, column=0)
        
        # Home welcome message
        tk.Label(center_frame, text="🏡 Welcome to the Home Page!", 
            font=("Arial", 24, "bold"), fg="#333333", bg="white").pack(pady=10)
        
        # Hyperlink with improved styling
        my_link = tk.Label(center_frame, text="Click Here For Live Reading Website", 
                    font=("Arial", 16), fg="#0066cc", cursor="hand2", bg="white")
        my_link.pack(pady=10)
        
        # Add underline effect on hover
        def on_enter(e):
            my_link.config(font=("Arial", 16, "underline"))
        
        def on_leave(e):
            my_link.config(font=("Arial", 16))
        
        my_link.bind('<Enter>', on_enter)
        my_link.bind('<Leave>', on_leave)
        my_link.bind('<Button-1>', lambda x: webbrowser.open_new("https://fyp-backend-bd5cc.web.app/base"))

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
        title_frame = tk.Frame(content_frame, bg="#e8eaf6")
        title_frame.grid(row=0, column=0, sticky="ew")
        
        # Configure grid for title frame
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        
        # Add title
        tk.Label(title_frame, text="📡 Live Sensor Readings", 
              font=("Arial", 18, "bold"), fg="black", bg="#e8eaf6").grid(row=0, column=0, pady=10)

        # Main content container for sensors
        reading_container = tk.Frame(content_frame, bg="white", height=412)
        reading_container.grid(row=1, column=0, sticky="nsew")
        reading_container.grid_propagate(False)
        
        # Configure grid for the reading container - two equal columns
        reading_container.columnconfigure(0, weight=1)  # Left sensor column
        reading_container.columnconfigure(1, weight=1)  # Right sensor column
        reading_container.rowconfigure(0, weight=1)     # Full height
        
        # Left side - DHT22 Sensor
        dht22_frame = tk.Frame(reading_container, bg="#e0f7fa")
        dht22_frame.grid(row=0, column=0, sticky="nsew")
        dht22_frame.grid_propagate(False)
        
        # Configure grid for DHT22 frame
        dht22_frame.columnconfigure(0, weight=1)  # Center column
        dht22_frame.rowconfigure(0, weight=0)     # Title row
        dht22_frame.rowconfigure(1, weight=1)     # Content row
        
        # DHT22 Title
        tk.Label(dht22_frame, text="🌡️ DHT22 Sensor", 
              font=("Arial", 16, "bold"), fg="black", bg="#e0f7fa").grid(row=0, column=0, pady=20)

        # DHT22 content frame
        dht_content = tk.Frame(dht22_frame, bg="#e0f7fa")
        dht_content.grid(row=1, column=0)
        
        # Configure grid for DHT content
        dht_content.columnconfigure(0, weight=1)
        for i in range(4):  # 4 rows for temperature and humidity labels and values
            dht_content.rowconfigure(i, weight=1)

        # Temperature and Humidity display
        temperature_label = tk.Label(content_frame, text="Temperature:", font=("Arial", 16, "bold"),  bg="#e0f7fa")
        temperature_value = tk.Label(content_frame, text="--°C", font=("Arial", 24), fg= "red", bg="#e0f7fa")
        temperature_label.grid(row=0, column=0, pady=(20, 0))
        temperature_value.grid(row=1, column=0, pady=(5, 20))

        humidity_label = tk.Label(content_frame, text="Humidity:", font=("Arial", 16, "bold"),bg="#e0f7fa")
        humidity_value = tk.Label(content_frame, text="--%", font=("Arial", 24), bg="#e0f7fa")
        humidity_label.grid(row=2, column=0, pady=(20, 0))
        humidity_value.grid(row=3, column=0, pady=(5, 20))

        # Start updating sensor readings
        update_DHT_sensor_readings()

        # Right side - Motion Sensor
        motion_frame = tk.Frame(reading_container, bg="#fce4ec")
        motion_frame.grid(row=0, column=1, sticky="nsew")
        motion_frame.grid_propagate(False)
        
        # Configure grid for motion frame
        motion_frame.columnconfigure(0, weight=1)  # Center column
        motion_frame.rowconfigure(0, weight=0)     # Title row
        motion_frame.rowconfigure(1, weight=1)     # Content row
        
        # Motion sensor title
        tk.Label(motion_frame, text="🔄 Motion Sensor (MPU6050)", 
              font=("Arial", 16, "bold"), fg="black", bg="#fce4ec").grid(row=0, column=0, pady=20)

        # Motion content frame
        motion_content = tk.Frame(motion_frame, bg="#fce4ec")
        motion_content.grid(row=1, column=0)
        
        # Configure grid for motion content - two columns for accel and gyro
        motion_content.columnconfigure(0, weight=1)  # Accel column
        motion_content.columnconfigure(1, weight=1)  # Gyro column
        motion_content.rowconfigure(0, weight=1)     # Full height
        
        # Acceleration column
        accel_frame = tk.Frame(motion_content, bg="#fce4ec")
        accel_frame.grid(row=0, column=0, padx=30)
        
        # Configure grid for acceleration frame
        accel_frame.columnconfigure(0, weight=1)
        for i in range(4):  # 4 rows: title and 3 values
            accel_frame.rowconfigure(i, weight=1)
        
        # Acceleration title and values
        tk.Label(accel_frame, text="Acceleration:", 
             font=("Arial", 16, "bold"), bg="#fce4ec").grid(row=0, column=0, pady=(0, 10))
        
        accel_x = tk.Label(accel_frame, text="X: --", font=("Arial", 14), bg="#fce4ec", fg = "#553e1c")
        accel_y = tk.Label(accel_frame, text="Y: --", font=("Arial", 14), bg="#fce4ec", fg = "#553e1c")
        accel_z = tk.Label(accel_frame, text="Z: --", font=("Arial", 14), bg="#fce4ec", fg = "#553e1c")
        
        accel_x.grid(row=1, column=0, pady=5)
        accel_y.grid(row=2, column=0, pady=5)
        accel_z.grid(row=3, column=0, pady=5)
        
        # Gyroscope column
        gyro_frame = tk.Frame(motion_content, bg="#fce4ec")
        gyro_frame.grid(row=0, column=1, padx=30)
        
        # Configure grid for gyroscope frame
        gyro_frame.columnconfigure(0, weight=1)
        for i in range(4):  # 4 rows: title and 3 values
            gyro_frame.rowconfigure(i, weight=1)
        
        # Gyroscope title and values
        tk.Label(gyro_frame, text="Gyroscope:", 
             font=("Arial", 16, "bold"), bg="#fce4ec").grid(row=0, column=0, pady=(0, 10))
        
        gyro_x = tk.Label(gyro_frame, text="X: --", font=("Arial", 14), bg="#fce4ec", fg ="#758b42")
        gyro_y = tk.Label(gyro_frame, text="Y: --", font=("Arial", 14), bg="#fce4ec", fg ="#758b42")
        gyro_z = tk.Label(gyro_frame, text="Z: --", font=("Arial", 14), bg="#fce4ec", fg ="#758b42")
        
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
        tk.Label(content_frame, text="🔧 Debug Mode", 
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
        debug_led_button = tk.Button(content_frame, text="Debug LED", command=lambda: run_debug("led"), **button_style)
        debug_led_button.grid(row=1, column=0, padx=30, pady=30, sticky="nsew")
        
        # Top right - Debug Button
        debug_button_button = tk.Button(content_frame, text="Debug Button", command=lambda: run_debug("button"), **button_style)
        debug_button_button.grid(row=1, column=1, padx=30, pady=30, sticky="nsew")
        
        # Bottom left - Debug DHT22
        debug_dht22_button = tk.Button(content_frame, text="Debug DHT22", command=lambda: run_debug("dht22"), **button_style)
        debug_dht22_button.grid(row=2, column=0, padx=30, pady=30, sticky="nsew")
        
        # Bottom right - Debug Motion Sensor
        debug_motion_button = tk.Button(content_frame, text="Debug Motion", command=lambda: run_debug("motion"), **button_style)
        debug_motion_button.grid(row=2, column=1, padx=30, pady=30, sticky="nsew")
        
        # Middle button - Run all debug tests
        all_debug_button = tk.Button(content_frame, text="Run All Debug Tests", 
                            command=lambda: run_debug("all"), 
                            bg="#007acc", 
                            fg="white", 
                            font=("Arial", 16, "bold"),
                            padx=20, 
                            pady=10,
                            width=20)
        all_debug_button.grid(row=3, column=0, columnspan=2, pady=30)

def run_debug(debug_type):
    if debug_type == "led":
        # Create a pop-up window for LED debugging
        led_window = tk.Toplevel()
        led_window.title("Debug LED")
        led_window.geometry("500x300")
        led_window.configure(bg="#f0f0f0")
        
        # Make the window modal (user must interact with it before returning to main app)
        led_window.grab_set()
        
        # Center the window on screen
        led_window.update_idletasks()
        width = led_window.winfo_width()
        height = led_window.winfo_height()
        x = (led_window.winfo_screenwidth() // 2) - (width // 2)
        y = (led_window.winfo_screenheight() // 2) - (height // 2)
        led_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Variables to track the state of each LED
        led_responses = [tk.BooleanVar() for _ in range(3)]  # For Red, Blue, Green LEDs
        current_led_index = [0]  # Using list to make it mutable in nested functions
        
        # Function to handle the LED diagnostics flow
        def check_led_response():
            if current_led_index[0] < len(led_responses):
                # Turn on the current LED
                led_pin = [17, 27, 22][current_led_index[0]]  # Red, Blue, Green
                GPIO.output(led_pin, 1)
                
                # Update the question text for the current LED
                led_colors = ["Red", "Blue", "Green"]
                question_label.config(text=f"Is the {led_colors[current_led_index[0]]} LED (Pin {led_pin}) illuminated?")
                
                # Show the question frame
                question_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            else:
                # All LEDs have been checked
                show_results()
        
        def led_response(is_working):
            # Record the response for the current LED
            led_responses[current_led_index[0]].set(is_working)
            
            # Turn off the current LED
            led_pin = [17, 27, 22][current_led_index[0]]
            GPIO.output(led_pin, 0)
            
            # Hide the question frame
            question_frame.pack_forget()
            
            # Move to the next LED
            current_led_index[0] += 1
            
            # Check the next LED or show results
            check_led_response()
        
        def show_results():
            # Check if all LEDs are working
            all_working = all([led.get() for led in led_responses])
            
            if all_working:
                # Show success message
                success_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            else:
                # Show error message
                error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                # Determine which LEDs are not working
                led_colors = ["Red", "Blue", "Green"]
                not_working = [led_colors[i] for i in range(len(led_responses)) if not led_responses[i].get()]
                
                error_label.config(text=f"The following LEDs are not working: {', '.join(not_working)}.\n"
                                       f"Please check the circuit connections for these LEDs and try again.")
        
        def close_window():
            led_window.grab_release()
            led_window.destroy()
        
        def start_test():
            # Hide the start frame
            start_frame.pack_forget()
            # Start the LED test
            check_led_response()
        
        # Create frames for each step of the diagnostic
        start_frame = tk.Frame(led_window, bg="#f0f0f0")
        question_frame = tk.Frame(led_window, bg="#f0f0f0")
        error_frame = tk.Frame(led_window, bg="#f0f0f0")
        success_frame = tk.Frame(led_window, bg="#f0f0f0")
        
        # Start frame
        tk.Label(start_frame, text="LED Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(start_frame, text="This test will check each LED in sequence.\n"
                              "You will need to confirm if each LED lights up.", 
              font=("Arial", 12), bg="#f0f0f0", justify=tk.LEFT).pack(pady=10)
        
        tk.Button(start_frame, text="Start Test", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
              command=start_test).pack(pady=20)
        
        # Question frame
        tk.Label(question_frame, text="LED Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        question_label = tk.Label(question_frame, text="", font=("Arial", 12), bg="#f0f0f0")
        question_label.pack(pady=10)
        
        button_frame = tk.Frame(question_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Yes", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
              command=lambda: led_response(True)).pack(side=LEFT, padx=10)
        tk.Button(button_frame, text="No", font=("Arial", 12), bg="#F44336", fg="white", width=10,
              command=lambda: led_response(False)).pack(side=LEFT, padx=10)
        
        # Error frame
        tk.Label(error_frame, text="Error Detected", font=("Arial", 16, "bold"), fg="#F44336", bg="#f0f0f0").pack(pady=10)
        error_label = tk.Label(error_frame, text="", font=("Arial", 12), bg="#f0f0f0", wraplength=400)
        error_label.pack(pady=10)
        
        # Add an icon or illustration for error
        tk.Label(error_frame, text="❌", font=("Arial", 48), fg="#F44336", bg="#f0f0f0").pack(pady=10)
        
        tk.Button(error_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Success frame
        tk.Label(success_frame, text="Diagnostic Complete", font=("Arial", 16, "bold"), fg="#4CAF50", bg="#f0f0f0").pack(pady=10)
        tk.Label(success_frame, text="All LEDs are working correctly!", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        # Add an icon or illustration for success
        tk.Label(success_frame, text="✅", font=("Arial", 48), fg="#4CAF50", bg="#f0f0f0").pack(pady=10)
        
        tk.Button(success_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Start with the start frame
        start_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
    
    elif debug_type == "button":
         # Create a pop-up window for Button debugging
        button_window = tk.Toplevel()
        button_window.title("Debug Button")
        button_window.geometry("500x300")
        button_window.configure(bg="#f0f0f0")
        
        # Make the window modal (user must interact with it before returning to main app)
        button_window.grab_set()
        
        # Center the window on screen
        button_window.update_idletasks()
        width = button_window.winfo_width()
        height = button_window.winfo_height()
        x = (button_window.winfo_screenwidth() // 2) - (width // 2)
        y = (button_window.winfo_screenheight() // 2) - (height // 2)
        button_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Variables to track the state of each button
        button_responses = [tk.BooleanVar() for _ in range(2)]  # For Red, Blue, Green LEDs
        current_button_index = [0]  # Using list to make it mutable in nested functions
        button_pins = [10, 9]
        def button_pressed(pin):
            # This function will be called when GPIO detects a button press
            if current_button_index[0] < len(button_responses) and pin == button_pins[current_button_index[0]]:
                # Record that the button was successfully pressed
                button_responses[current_button_index[0]].set(True)
                
                # Update status label
                status_label.config(text="Button press detected! ✅", fg="#4CAF50")
                
                # Enable the Next/Finish button
                if current_button_index[0] == len(button_responses) - 1:
                    next_button.config(text="Finish", state=NORMAL)
                else:
                    next_button.config(state=NORMAL)
        
        def setup_button_detection():
            # Set up GPIO event detection for the current button
            pin = button_pins[current_button_index[0]]
            GPIO.remove_event_detect(pin)  # Remove any existing detection
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_pressed, bouncetime=300)
        
        def move_to_next_button():
            # If user clicked "No Response", record failure
            if not button_responses[current_button_index[0]].get():
                button_responses[current_button_index[0]].set(False)
            
            # Remove event detection for current button
            GPIO.remove_event_detect(button_pins[current_button_index[0]])
            
            # Move to next button or show results
            current_button_index[0] += 1
            
            if current_button_index[0] < len(button_responses):
                # Test the next button
                test_current_button()
            else:
                # All buttons have been tested
                show_results()
        
        def test_current_button():
            # Hide the start frame if visible
            start_frame.pack_forget()
            
            # Update the question for the current button
            button_names = ["first (GPIO 10)", "second (GPIO 9)"]
            question_label.config(text=f"Please press the {button_names[current_button_index[0]]} button")
            
            # Reset status label
            status_label.config(text="Waiting for button press...", fg="#666666")
            
            # Disable the Next button until button press is detected
            next_button.config(text="Next", state=DISABLED)
            
            # Set up GPIO detection for this button
            setup_button_detection()
            
            # Show the question frame
            question_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        def no_response():
            # Record that the button did not work
            button_responses[current_button_index[0]].set(False)
            
            # Enable the Next/Finish button
            if current_button_index[0] == len(button_responses) - 1:
                next_button.config(text="Finish", state=NORMAL)
            else:
                next_button.config(state=NORMAL)
        
        def show_results():
            # Hide the question frame
            question_frame.pack_forget()
            
            # Check if all buttons are working
            all_working = all([button.get() for button in button_responses])
            
            if all_working:
                # Show success message
                success_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            else:
                # Show error message
                error_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                
                # Determine which buttons are not working
                button_names = ["GPIO 10 button", "GPIO 9 button"]
                not_working = [button_names[i] for i in range(len(button_responses)) if not button_responses[i].get()]
                
                error_label.config(text=f"The following buttons are not working: {', '.join(not_working)}.\n"
                                       f"Please check the circuit connections and try again.")
        
        def close_window():
            # Clean up GPIO event detection before closing
            for pin in button_pins:
                try:
                    GPIO.remove_event_detect(pin)
                except:
                    pass
            
            button_window.grab_release()
            button_window.destroy()
        
        def start_test():
            # Hide the start frame
            start_frame.pack_forget()
            # Start testing the first button
            test_current_button()
        
        # Create frames for each step of the diagnostic
        start_frame = tk.Frame(button_window, bg="#f0f0f0")
        question_frame = tk.Frame(button_window, bg="#f0f0f0")
        error_frame = tk.Frame(button_window, bg="#f0f0f0")
        success_frame = tk.Frame(button_window, bg="#f0f0f0")
        
        # Start frame
        tk.Label(start_frame, text="Button Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(start_frame, text="This test will check each button in sequence.\n"
                              "You will need to press each button when prompted.", 
              font=("Arial", 12), bg="#f0f0f0", justify=LEFT).pack(pady=10)
        
        tk.Button(start_frame, text="Start Test", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
              command=start_test).pack(pady=20)
        
        # Question frame
        tk.Label(question_frame, text="Button Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        question_label = tk.Label(question_frame, text="", font=("Arial", 12), bg="#f0f0f0")
        question_label.pack(pady=10)
        
        status_label = tk.Label(question_frame, text="Waiting for button press...", font=("Arial", 12), fg="#666666", bg="#f0f0f0")
        status_label.pack(pady=10)
        
        button_frame = tk.Frame(question_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="No Response", font=("Arial", 12), bg="#F44336", fg="white", width=12,
              command=no_response).pack(side=LEFT, padx=10)
              
        next_button = tk.Button(button_frame, text="Next", font=("Arial", 12), bg="#007acc", fg="white", width=10,
                           state=DISABLED, command=move_to_next_button)
        next_button.pack(side=LEFT, padx=10)
        
        # Error frame
        tk.Label(error_frame, text="Error Detected", font=("Arial", 16, "bold"), fg="#F44336", bg="#f0f0f0").pack(pady=10)
        error_label = tk.Label(error_frame, text="", font=("Arial", 12), bg="#f0f0f0", wraplength=400)
        error_label.pack(pady=10)
        
        # Add an icon or illustration for error
        tk.Label(error_frame, text="❌", font=("Arial", 48), fg="#F44336", bg="#f0f0f0").pack(pady=10)
        
        tk.Button(error_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Success frame
        tk.Label(success_frame, text="Diagnostic Complete", font=("Arial", 16, "bold"), fg="#4CAF50", bg="#f0f0f0").pack(pady=10)
        tk.Label(success_frame, text="All buttons are working correctly!", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        # Add an icon or illustration for success
        tk.Label(success_frame, text="✅", font=("Arial", 48), fg="#4CAF50", bg="#f0f0f0").pack(pady=10)
        
        tk.Button(success_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Start with the start frame
        start_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    
    elif debug_type == "dht22":
        # Create a pop-up window for DHT22 debugging
        dht_window = tk.Toplevel()
        dht_window.title("Debug DHT22 Sensor")
        dht_window.geometry("550x400")
        dht_window.configure(bg="#f0f0f0")
        
        # Make the window modal
        dht_window.grab_set()
        
        # Center the window on screen
        dht_window.update_idletasks()
        width = dht_window.winfo_width()
        height = dht_window.winfo_height()
        x = (dht_window.winfo_screenwidth() // 2) - (width // 2)
        y = (dht_window.winfo_screenheight() // 2) - (height // 2)
        dht_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Variables to track sensor readings
        current_temp = tk.StringVar(value="--")
        current_humidity = tk.StringVar(value="--")
        test_results = {"connection": False, "temp_reading": False, "humid_reading": False}
        
        def check_sensor_connection():
            try:
                # Create a new instance to test (don't use the global one)
                test_dht = adafruit_dht.DHT22(board.D18)
                # Try to read from it
                test_dht.measure()
                
                # If no exception, connection is good
                test_results["connection"] = True
                connection_label.config(text="✅ Sensor connection OK", fg="#4CAF50")
                
                # Move to next stage
                check_temperature()
                
                # Clean up test sensor
                test_dht.exit()
                
            except Exception as e:
                # Connection failed
                connection_label.config(text="❌ Sensor connection failed", fg="#F44336")
                error_details.config(text=f"Error: {str(e)}\n\nSuggestions:\n• Check if sensor is properly connected to GPIO 18\n• Check for loose wires\n• Try using a different DHT22 sensor\n• Ensure power supply is adequate (3.3V)")
                
                # Show troubleshooting section
                troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
                
                # Disable Continue button, enable Retry button
                continue_button.config(state=tk.DISABLED)
                retry_button.config(state=tk.NORMAL)
        
        def check_temperature():
            try:
                # Try to read temperature
                temp = dhtDevice.temperature
                if temp is not None:
                    test_results["temp_reading"] = True
                    current_temp.set(f"{temp:.1f}°C")
                    temp_label.config(text=f"✅ Temperature reading OK: {temp:.1f}°C", fg="#4CAF50")
                else:
                    temp_label.config(text="❌ Temperature reading failed (null value)", fg="#F44336")
            except Exception as e:
                temp_label.config(text="❌ Temperature reading failed", fg="#F44336")
                error_details.config(text=f"Error: {str(e)}\n\nSuggestions:\n• Wait a few seconds and retry\n• Check for interference from other devices\n• Check for physical damage to the sensor\n• Try a slower read rate (DHT22 requires 2+ seconds between reads)")
                
                # Show troubleshooting section
                troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Always check humidity next
            check_humidity()
        
        def check_humidity():
            try:
                # Try to read humidity
                humidity = dhtDevice.humidity
                if humidity is not None:
                    test_results["humid_reading"] = True
                    current_humidity.set(f"{humidity:.1f}%")
                    humidity_label.config(text=f"✅ Humidity reading OK: {humidity:.1f}%", fg="#4CAF50")
                else:
                    humidity_label.config(text="❌ Humidity reading failed (null value)", fg="#F44336")
            except Exception as e:
                humidity_label.config(text="❌ Humidity reading failed", fg="#F44336")
                error_details.config(text=f"Error: {str(e)}\n\nSuggestions:\n• Wait a few seconds and retry\n• Check for interference from other devices\n• Check for physical damage to the sensor\n• Try a slower read rate (DHT22 requires 2+ seconds between reads)")
                
                # Show troubleshooting section
                troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Update the continue button based on test results
            if all(test_results.values()):
                continue_button.config(state=tk.NORMAL)
            else:
                continue_button.config(state=tk.DISABLED)
                retry_button.config(state=tk.NORMAL)
        
        def retry_tests():
            # Reset labels
            connection_label.config(text="Checking sensor connection...", fg="#666666")
            temp_label.config(text="Checking temperature reading...", fg="#666666")
            humidity_label.config(text="Checking humidity reading...", fg="#666666")
            
            # Reset test results
            for key in test_results:
                test_results[key] = False
            
            # Hide troubleshooting section
            troubleshooting_frame.pack_forget()
            
            # Disable buttons during test
            retry_button.config(state=tk.DISABLED)
            continue_button.config(state=tk.DISABLED)
            
            # Start tests again
            main_window.after(500, check_sensor_connection)
        
        def show_monitoring():
            # Hide diagnostic frame
            diagnostic_frame.pack_forget()
            
            # Show monitoring frame
            monitoring_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Start periodic monitoring
            update_monitor()
        
        def update_monitor():
            try:
                # Try to read values
                temp = dhtDevice.temperature
                humidity = dhtDevice.humidity
                
                if temp is not None and humidity is not None:
                    current_temp.set(f"{temp:.1f}°C")
                    current_humidity.set(f"{humidity:.1f}%")
                    status_label.config(text="Sensor working correctly ✅", fg="#4CAF50")
                else:
                    status_label.config(text="Error: Received null values ❌", fg="#F44336")
            except Exception as e:
                status_label.config(text=f"Error: {str(e)[:50]}... ❌", fg="#F44336")
            
            # Schedule next update (every 2 seconds to avoid overwhelming the sensor)
            if monitoring_frame.winfo_exists():  # Check if window still exists
                monitoring_frame.after(2000, update_monitor)
        
        def close_window():
            dht_window.grab_release()
            dht_window.destroy()
        
        # Create frames for each part of the diagnostic
        main_window = tk.Frame(dht_window, bg="#f0f0f0")
        diagnostic_frame = tk.Frame(main_window, bg="#f0f0f0")
        troubleshooting_frame = tk.Frame(main_window, bg="#f0f0f0")
        monitoring_frame = tk.Frame(main_window, bg="#f0f0f0")
        
        # Main title
        tk.Label(main_window, text="DHT22 Sensor Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Diagnostic frame
        diagnostic_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status labels for connection and readings
        connection_label = tk.Label(diagnostic_frame, text="Checking sensor connection...", font=("Arial", 12), fg="#666666", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        connection_label.pack(fill=tk.X, pady=(10, 5))
        
        temp_label = tk.Label(diagnostic_frame, text="Checking temperature reading...", font=("Arial", 12), fg="#666666", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        temp_label.pack(fill=tk.X, pady=5)
        
        humidity_label = tk.Label(diagnostic_frame, text="Checking humidity reading...", font=("Arial", 12), fg="#666666", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        humidity_label.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = tk.Frame(diagnostic_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        retry_button = tk.Button(button_frame, text="Retry", font=("Arial", 12), bg="#F44336", fg="white", width=10,
                             state=tk.DISABLED, command=retry_tests)
        retry_button.pack(side=tk.LEFT, padx=10)
        
        continue_button = tk.Button(button_frame, text="Continue", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
                                state=tk.DISABLED, command=show_monitoring)
        continue_button.pack(side=tk.LEFT, padx=10)
        
        # Troubleshooting frame
        tk.Label(troubleshooting_frame, text="Troubleshooting", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        error_details = tk.Label(troubleshooting_frame, text="", font=("Arial", 11), bg="#f0f0f0", anchor="w", justify=tk.LEFT, wraplength=500)
        error_details.pack(fill=tk.X, pady=5)
        
        # Monitoring frame
        tk.Label(monitoring_frame, text="DHT22 Continuous Monitoring", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Current values with larger display
        tk.Label(monitoring_frame, text="Current Temperature:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))
        tk.Label(monitoring_frame, textvariable=current_temp, font=("Arial", 24, "bold"), fg="#FF5722", bg="#f0f0f0").pack()
        
        tk.Label(monitoring_frame, text="Current Humidity:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(20, 0))
        tk.Label(monitoring_frame, textvariable=current_humidity, font=("Arial", 24, "bold"), fg="#2196F3", bg="#f0f0f0").pack()
        
        # Status label
        status_label = tk.Label(monitoring_frame, text="Monitoring...", font=("Arial", 12), fg="#666666", bg="#f0f0f0")
        status_label.pack(pady=20)
        
        # Close button
        tk.Button(monitoring_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Pack the main window
        main_window.pack(fill=tk.BOTH, expand=True)
        
        # Start the diagnostics
        check_sensor_connection()
    
    elif debug_type == "motion":
        # Create a pop-up window for Motion Sensor debugging
        motion_window = tk.Toplevel()
        motion_window.title("Debug Motion Sensor (MPU6050)")
        motion_window.geometry("600x500")
        motion_window.configure(bg="#f0f0f0")
        
        # Make the window modal
        motion_window.grab_set()
        
        # Center the window on screen
        motion_window.update_idletasks()
        width = motion_window.winfo_width()
        height = motion_window.winfo_height()
        x = (motion_window.winfo_screenwidth() // 2) - (width // 2)
        y = (motion_window.winfo_screenheight() // 2) - (height // 2)
        motion_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Test results tracking
        test_results = {"connection": False, "accel": False, "gyro": False}
        
        # Variables for current values
        accel_values = {"x": tk.DoubleVar(value=0), "y": tk.DoubleVar(value=0), "z": tk.DoubleVar(value=0)}
        gyro_values = {"x": tk.DoubleVar(value=0), "y": tk.DoubleVar(value=0), "z": tk.DoubleVar(value=0)}
        
        def check_sensor_connection():
            try:
                # Test connection by trying to read data
                test_mpu = mpu6050.mpu6050(0x68)
                test_data = test_mpu.get_temp()
                
                # If no exception, connection is good
                test_results["connection"] = True
                connection_label.config(text="✅ Sensor connection OK (I2C Address: 0x68)", fg="#4CAF50")
                
                # Move to check accelerometer
                check_accelerometer()
                
            except Exception as e:
                # Connection failed
                connection_label.config(text="❌ Sensor connection failed", fg="#F44336")
                error_details.config(text=f"Error: {str(e)}\n\nSuggestions:\n• Check I2C connections (SDA/SCL)\n• Verify I2C address (usually 0x68 or 0x69)\n• Check for loose wires\n• Ensure power supply is adequate\n• Verify I2C is enabled in raspi-config")
                
                # Show troubleshooting section
                troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
                
                # Disable Continue button, enable Retry button
                continue_button.config(state=tk.DISABLED)
                retry_button.config(state=tk.NORMAL)
        
        def check_accelerometer():
            try:
                # Try to read accelerometer data
                accel_data = mpu6050.get_accel_data()
                
                # Check if we got valid data (non-zero and not None)
                if accel_data and any(abs(accel_data[axis]) > 0.01 for axis in ['x', 'y', 'z']):
                    test_results["accel"] = True
                    accel_label.config(text=f"✅ Accelerometer readings OK: X={accel_data['x']:.2f}, Y={accel_data['y']:.2f}, Z={accel_data['z']:.2f}", fg="#4CAF50")
                    
                    # Update variables
                    for axis in ['x', 'y', 'z']:
                        accel_values[axis].set(accel_data[axis])
                else:
                    accel_label.config(text="❌ Accelerometer readings invalid (all zero or null)", fg="#F44336")
                    error_details.config(text="Suggestions:\n• Verify sensor is not damaged\n• Check power connections\n• Try reinitializing the sensor\n• Ensure sensor is properly seated on breakout board")
                    troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            except Exception as e:
                accel_label.config(text="❌ Error reading accelerometer data", fg="#F44336")
                error_details.config(text=f"Error: {str(e)}\n\nSuggestions:\n• Check for software conflicts\n• Verify I2C speed isn't too high\n• Try reinitializing the sensor\n• Check if sensor is defective")
                troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Check gyroscope next
            check_gyroscope()
        
        def check_gyroscope():
            try:
                # Try to read gyroscope data
                gyro_data = mpu6050.get_gyro_data()
                
                # Check if we got valid data
                if gyro_data and all(isinstance(gyro_data[axis], (int, float)) for axis in ['x', 'y', 'z']):
                    test_results["gyro"] = True
                    gyro_label.config(text=f"✅ Gyroscope readings OK: X={gyro_data['x']:.2f}, Y={gyro_data['y']:.2f}, Z={gyro_data['z']:.2f}", fg="#4CAF50")
                    
                    # Update variables
                    for axis in ['x', 'y', 'z']:
                        gyro_values[axis].set(gyro_data[axis])
                else:
                    gyro_label.config(text="❌ Gyroscope readings invalid (null or non-numeric)", fg="#F44336")
                    error_details.config(text="Suggestions:\n• Verify sensor is not damaged\n• Check power connections\n• Try reinitializing the sensor\n• Ensure sensor is properly seated on breakout board")
                    troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            except Exception as e:
                gyro_label.config(text="❌ Error reading gyroscope data", fg="#F44336")
                error_details.config(text=f"Error: {str(e)}\n\nSuggestions:\n• Check for software conflicts\n• Verify I2C speed isn't too high\n• Try reinitializing the sensor\n• Check if sensor is defective")
                troubleshooting_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Update the continue button based on test results
            if all(test_results.values()):
                continue_button.config(state=tk.NORMAL)
            else:
                continue_button.config(state=tk.DISABLED)
                retry_button.config(state=tk.NORMAL)
        
        def retry_tests():
            # Reset labels
            connection_label.config(text="Checking sensor connection...", fg="#666666")
            accel_label.config(text="Checking accelerometer readings...", fg="#666666")
            gyro_label.config(text="Checking gyroscope readings...", fg="#666666")
            
            # Reset test results
            for key in test_results:
                test_results[key] = False
            
            # Hide troubleshooting section
            troubleshooting_frame.pack_forget()
            
            # Disable buttons during test
            retry_button.config(state=tk.DISABLED)
            continue_button.config(state=tk.DISABLED)
            
            # Start tests again
            main_window.after(500, check_sensor_connection)
        
        def show_monitoring():
            # Hide diagnostic frame
            diagnostic_frame.pack_forget()
            
            # Show monitoring frame
            monitoring_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Start periodic monitoring
            update_monitor()
        
        def update_monitor():
            try:
                # Get latest sensor data
                accel_data = mpu6050.get_accel_data()
                gyro_data = mpu6050.get_gyro_data()
                
                # Update all values
                for axis in ['x', 'y', 'z']:
                    accel_values[axis].set(accel_data[axis])
                    gyro_values[axis].set(gyro_data[axis])
                
                # Update max values in acceleration bars
                for axis in ['x', 'y', 'z']:
                    current_val = abs(accel_data[axis])
                    # Scale to 0-100 range (assuming ±2g range)
                    scaled_val = min(100, int((current_val / 20) * 100))  
                    accel_bars[axis].config(value=scaled_val)
                
                # Update max values in gyroscope bars
                for axis in ['x', 'y', 'z']:
                    current_val = abs(gyro_data[axis])
                    # Scale to 0-100 range (assuming ±250 deg/s range)
                    scaled_val = min(100, int((current_val / 250) * 100))
                    gyro_bars[axis].config(value=scaled_val)
                
                status_label.config(text="Sensor working correctly ✅", fg="#4CAF50")
                
            except Exception as e:
                status_label.config(text=f"Error: {str(e)[:50]}... ❌", fg="#F44336")
            
            # Schedule next update if window still exists
            if monitoring_frame.winfo_exists():
                monitoring_frame.after(100, update_monitor)  # Update more frequently for motion sensor
        
        def close_window():
            motion_window.grab_release()
            motion_window.destroy()
        
        # Create frames
        main_window = tk.Frame(motion_window, bg="#f0f0f0")
        diagnostic_frame = tk.Frame(main_window, bg="#f0f0f0")
        troubleshooting_frame = tk.Frame(main_window, bg="#f0f0f0")
        monitoring_frame = tk.Frame(main_window, bg="#f0f0f0")
        
        # Main title
        tk.Label(main_window, text="MPU6050 Motion Sensor Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Diagnostic frame
        diagnostic_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status labels for connection and readings
        connection_label = tk.Label(diagnostic_frame, text="Checking sensor connection...", font=("Arial", 12), fg="#666666", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        connection_label.pack(fill=tk.X, pady=(10, 5))
        
        accel_label = tk.Label(diagnostic_frame, text="Checking accelerometer readings...", font=("Arial", 12), fg="#666666", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        accel_label.pack(fill=tk.X, pady=5)
        
        gyro_label = tk.Label(diagnostic_frame, text="Checking gyroscope readings...", font=("Arial", 12), fg="#666666", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        gyro_label.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = tk.Frame(diagnostic_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        retry_button = tk.Button(button_frame, text="Retry", font=("Arial", 12), bg="#F44336", fg="white", width=10,
                            state=tk.DISABLED, command=retry_tests)
        retry_button.pack(side=tk.LEFT, padx=10)
        
        continue_button = tk.Button(button_frame, text="Continue", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
                               state=tk.DISABLED, command=show_monitoring)
        continue_button.pack(side=tk.LEFT, padx=10)
        
        # Troubleshooting frame
        tk.Label(troubleshooting_frame, text="Troubleshooting", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        error_details = tk.Label(troubleshooting_frame, text="", font=("Arial", 11), bg="#f0f0f0", anchor="w", justify=tk.LEFT, wraplength=540)
        error_details.pack(fill=tk.X, pady=5)
        
        # Monitoring frame - using a more advanced layout with progress bars
        tk.Label(monitoring_frame, text="MPU6050 Motion Monitor", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Create two sections for accel and gyro
        monitor_container = tk.Frame(monitoring_frame, bg="#f0f0f0")
        monitor_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        accel_frame = tk.LabelFrame(monitor_container, text="Accelerometer", bg="#f0f0f0", font=("Arial", 12, "bold"))
        accel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        gyro_frame = tk.LabelFrame(monitor_container, text="Gyroscope", bg="#f0f0f0", font=("Arial", 12, "bold"))
        gyro_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Progress bars for each axis
        accel_bars = {}
        gyro_bars = {}
        
        from tkinter import ttk
        
        # Accelerometer readings and bars
        for i, axis in enumerate(['x', 'y', 'z']):
            frame = tk.Frame(accel_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=f"{axis.upper()}: ", width=3, bg="#f0f0f0").pack(side=tk.LEFT)
            tk.Label(frame, textvariable=accel_values[axis], width=8, bg="#f0f0f0").pack(side=tk.LEFT)
            
            # Add a progress bar
            bar = ttk.Progressbar(frame, length=150, mode="determinate")
            bar.pack(side=tk.LEFT, padx=5)
            accel_bars[axis] = bar
        
        # Gyroscope readings and bars
        for i, axis in enumerate(['x', 'y', 'z']):
            frame = tk.Frame(gyro_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=f"{axis.upper()}: ", width=3, bg="#f0f0f0").pack(side=tk.LEFT)
            tk.Label(frame, textvariable=gyro_values[axis], width=8, bg="#f0f0f0").pack(side=tk.LEFT)
            
            # Add a progress bar
            bar = ttk.Progressbar(frame, length=150, mode="determinate")
            bar.pack(side=tk.LEFT, padx=5)
            gyro_bars[axis] = bar
        
        # Status label
        status_label = tk.Label(monitoring_frame, text="Initializing...", font=("Arial", 12), fg="#666666", bg="#f0f0f0")
        status_label.pack(pady=10)
        
        # Tilt indicator - using a basic visual representation
        tilt_frame = tk.LabelFrame(monitoring_frame, text="Orientation", bg="#f0f0f0", font=("Arial", 12, "bold"))
        tilt_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tilt_canvas = tk.Canvas(tilt_frame, width=100, height=100, bg="white", highlightthickness=0)
        tilt_canvas.pack(pady=10)
        
        # Draw a basic orientation indicator
        center_x, center_y = 50, 50
        indicator = tilt_canvas.create_oval(center_x-5, center_y-5, center_x+5, center_y+5, fill="red")
        
        # X and Y axis lines
        tilt_canvas.create_line(0, center_y, 100, center_y, dash=(2, 2))
        tilt_canvas.create_line(center_x, 0, center_x, 100, dash=(2, 2))
        
        # Close button
        tk.Button(monitoring_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Pack the main window
        main_window.pack(fill=tk.BOTH, expand=True)
        
        # Start the diagnostics
        check_sensor_connection()
    
    elif debug_type == "all":
        messagebox.showinfo("Debug All", "Running all debug tests sequentially")

        def run_all_tests():
            run_debug("led")
            window.after(3000, lambda: run_debug("button"))
            window.after(6000, lambda: run_debug("dht22"))
            window.after(9000, lambda: run_debug("motion"))

        window.after(1000, run_all_tests)  # Start after a small delay
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

#GPIO Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=0)
GPIO.setup(27, GPIO.OUT, initial=0)
GPIO.setup(22, GPIO.OUT, initial=0)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Configuration 
dhtDevice = adafruit_dht.DHT22(board.D18)
mpu6050 = mpu6050.mpu6050(0x68) #0x68 is the i2c address

# Main Window
window = tk.Tk()
window.title("Kai Sheng's Mini Project")
window.geometry('1024x512')
window.resizable(False, False)  
window.configure(bg="#f0f0f0")
window.columnconfigure(0, weight=1)  # Configure grid for window
window.rowconfigure(0, weight=0)     # Nav bar row
window.rowconfigure(1, weight=1)     # Content row

# Navigation Bar
nav_frame = tk.Frame(window, bg="#007acc", height=50)
nav_frame.grid(row=0, column=0, sticky="ew")

# Configure grid for nav frame - three columns for buttons
nav_frame.columnconfigure(0, weight=0)  # Home button
nav_frame.columnconfigure(1, weight=0)  # Reading button
nav_frame.columnconfigure(2, weight=0)  # Debug button
nav_frame.columnconfigure(3, weight=1)  # Empty space
nav_frame.rowconfigure(0, weight=1)     # Single row

# Navigation Buttons
tk.Button(nav_frame, text="🏡 Home", font=("Arial", 14, "bold"), bg="#005a9e", fg="white",
       padx=30, pady=10, command=lambda: show_content("Home")).grid(row=0, column=0)

tk.Button(nav_frame, text="📡 Reading", font=("Arial", 14, "bold"), bg="#005a9e", fg="white",
       padx=30, pady=10, command=lambda: show_content("Reading")).grid(row=0, column=1, padx=50)

tk.Button(nav_frame, text="🔧 Debug", font=("Arial", 14, "bold"), bg="#005a9e", fg="white",
       padx=30, pady=10, command=lambda: show_content("Debug")).grid(row=0, column=2)

# Main content area
main_frame = Frame(window, bg="white")
main_frame.grid(row=1, column=0, sticky="nsew")

# Configure grid for main frame
main_frame.columnconfigure(0, weight=1)  # Canvas column
main_frame.columnconfigure(1, weight=0)  # Scrollbar column
main_frame.rowconfigure(0, weight=1)     # Single row

# Canvas and scrollbar
canvas = tk.Canvas(main_frame, bg="white")
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

# Configure canvas
canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = tk.Frame(canvas, bg="white")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
window_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Position canvas and scrollbar with grid
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Configure grid for scrollable frame
scrollable_frame.columnconfigure(0, weight=1)
scrollable_frame.rowconfigure(0, weight=1)

# Content frame inside Scrollable Frame
content_frame = tk.Frame(scrollable_frame, bg="white")
content_frame.grid(row=0, column=0, sticky="nsew")


# Load Home Page by default
show_content("Home")

# Run GUI
window.mainloop()