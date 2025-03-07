import tkinter as tk
import subprocess
from tkinter import *
import webbrowser
from tkinter import messagebox

def show_content(page):
    # Clear previous content
    for widget in content_frame.winfo_children():
        widget.destroy()

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
        center_frame = Frame(content_frame, bg="white")
        center_frame.grid(row=0, column=0)
        
        # Home welcome message
        Label(center_frame, text="🏡 Welcome to the Home Page!", 
            font=("Arial", 24, "bold"), fg="#333333", bg="white").pack(pady=10)
        
        # Hyperlink with improved styling
        my_link = Label(center_frame, text="Click Here For Live Reading Website", 
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
        title_frame = Frame(content_frame, bg="#e8eaf6")
        title_frame.grid(row=0, column=0, sticky="ew")
        
        # Configure grid for title frame
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        
        # Add title
        Label(title_frame, text="📡 Live Sensor Readings", 
              font=("Arial", 18, "bold"), fg="black", bg="#e8eaf6").grid(row=0, column=0, pady=10)

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


        # Temperature section
        temperature_label = Label(dht_content, text="Temperature:", 
                                 font=("Arial", 16, "bold"), bg="#e0f7fa")
        temperature_value = Label(dht_content, text="25°C", 
                                 font=("Arial", 24), bg="#e0f7fa", fg="blue")
        
        temperature_label.grid(row=0, column=0, pady=(20, 0))
        temperature_value.grid(row=1, column=0, pady=(5, 20))
        
        # Humidity section
        humidity_label = Label(dht_content, text="Humidity:", 
                              font=("Arial", 16, "bold"), bg="#e0f7fa")
        humidity_value = Label(dht_content, text="60%", 
                              font=("Arial", 24), bg="#e0f7fa", fg = "#ffd180")
        
        humidity_label.grid(row=2, column=0, pady=(20, 0))
        humidity_value.grid(row=3, column=0, pady=(5, 20))

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
        
        accel_x = Label(accel_frame, text="X: 0.98", font=("Arial", 14), bg="#fce4ec", fg = "#553e1c")
        accel_y = Label(accel_frame, text="Y: 0.05", font=("Arial", 14), bg="#fce4ec", fg = "#553e1c")
        accel_z = Label(accel_frame, text="Z: -0.02", font=("Arial", 14), bg="#fce4ec", fg = "#553e1c")
        
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
        
        gyro_x = Label(gyro_frame, text="X: 0.10", font=("Arial", 14), bg="#fce4ec", fg ="#758b42")
        gyro_y = Label(gyro_frame, text="Y: 0.15", font=("Arial", 14), bg="#fce4ec", fg ="#758b42")
        gyro_z = Label(gyro_frame, text="Z: 0.05", font=("Arial", 14), bg="#fce4ec", fg ="#758b42")
        
        gyro_x.grid(row=1, column=0, pady=5)
        gyro_y.grid(row=2, column=0, pady=5)
        gyro_z.grid(row=3, column=0, pady=5)

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

def run_debug(debug_type):
    if debug_type == "led":
        # Create a pop-up window for LED debugging
        led_window = Toplevel()
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
        first_led_ok = BooleanVar()
        second_led_ok = BooleanVar()
        
        # Function to handle the LED diagnostics flow
        def check_first_led():
            first_frame.pack_forget()
            if first_led_ok.get():
                # If first LED is OK, check second LED
                second_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            else:
                # If first LED is not OK, show error message
                error_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                error_label.config(text="First LED is not working.\nPlease check the circuit connection and try again.")
        
        def check_second_led():
            second_frame.pack_forget()
            if second_led_ok.get():
                # If second LED is OK, show success message
                success_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            else:
                # If second LED is not OK, show error message
                error_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
                error_label.config(text="Second LED is not working.\nPlease check the circuit connection and try again.")
        
        def close_window():
            led_window.grab_release()
            led_window.destroy()
        
        # Create frames for each step of the diagnostic
        first_frame = Frame(led_window, bg="#f0f0f0")
        second_frame = Frame(led_window, bg="#f0f0f0")
        error_frame = Frame(led_window, bg="#f0f0f0")
        success_frame = Frame(led_window, bg="#f0f0f0")
        
        # First LED check
        Label(first_frame, text="LED Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        Label(first_frame, text="Is the first LED (Red) illuminated?", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        button_frame1 = Frame(first_frame, bg="#f0f0f0")
        button_frame1.pack(pady=20)
        
        Button(button_frame1, text="Yes", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
              command=lambda: [first_led_ok.set(True), check_first_led()]).pack(side=LEFT, padx=10)
        Button(button_frame1, text="No", font=("Arial", 12), bg="#F44336", fg="white", width=10,
              command=lambda: [first_led_ok.set(False), check_first_led()]).pack(side=LEFT, padx=10)
        
        # Second LED check
        Label(second_frame, text="LED Diagnostic", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        Label(second_frame, text="Is the second LED (Green) illuminated?", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        button_frame2 = Frame(second_frame, bg="#f0f0f0")
        button_frame2.pack(pady=20)
        
        Button(button_frame2, text="Yes", font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
              command=lambda: [second_led_ok.set(True), check_second_led()]).pack(side=LEFT, padx=10)
        Button(button_frame2, text="No", font=("Arial", 12), bg="#F44336", fg="white", width=10,
              command=lambda: [second_led_ok.set(False), check_second_led()]).pack(side=LEFT, padx=10)
        
        # Error frame
        Label(error_frame, text="Error Detected", font=("Arial", 16, "bold"), fg="#F44336", bg="#f0f0f0").pack(pady=10)
        error_label = Label(error_frame, text="", font=("Arial", 12), bg="#f0f0f0", wraplength=400)
        error_label.pack(pady=10)
        
        # Add an icon or illustration for error
        Label(error_frame, text="❌", font=("Arial", 48), fg="#F44336", bg="#f0f0f0").pack(pady=10)
        
        Button(error_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Success frame
        Label(success_frame, text="Diagnostic Complete", font=("Arial", 16, "bold"), fg="#4CAF50", bg="#f0f0f0").pack(pady=10)
        Label(success_frame, text="All LEDs are working correctly!", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        
        # Add an icon or illustration for success
        Label(success_frame, text="✅", font=("Arial", 48), fg="#4CAF50", bg="#f0f0f0").pack(pady=10)
        
        Button(success_frame, text="Close", font=("Arial", 12), bg="#555555", fg="white", width=10,
              command=close_window).pack(pady=10)
        
        # Start with the first frame
        first_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
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
        # DHT22 debugging code will go here (implement later)
        messagebox.showinfo("Debug DHT22", "DHT22 debugging will be implemented next")
    
    elif debug_type == "motion":
        # Motion sensor debugging code will go here (implement later)
        messagebox.showinfo("Debug Motion", "Motion sensor debugging will be implemented next")
    
    elif debug_type == "all":
        messagebox.showinfo("Debug All", "Running all debug tests sequentially")

        def run_all_tests():
            run_debug("led")
            window.after(3000, lambda: run_debug("button"))
            window.after(6000, lambda: run_debug("dht22"))
            window.after(9000, lambda: run_debug("motion"))

        window.after(1000, run_all_tests)  # Start after a small delay


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