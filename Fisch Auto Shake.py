import threading
import time
import tkinter as tk
from pynput.keyboard import Controller, Key, Listener
import pygetwindow as gw
import pyautogui

# Global variables
spamming = False
spam_speed = 0.01  # Default spam speed in seconds
stop_event = threading.Event()  # Event to stop the spam thread
keyboard_controller = Controller()
start_time = None  # To track the time when spamming starts

# Function to bring the target window to the foreground
def bring_window_to_front(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]  # Get window by title
        if window:
            window.activate()  # Bring the window to the foreground
    except IndexError:
        print(f"Window with title '{window_title}' not found.")
        
# Function to press and release keys continuously at a low level
def spam_keys(window_title):
    global start_time
    start_time = time.time()  # Start the timer when the spamming begins
    
    while not stop_event.is_set():
        bring_window_to_front(window_title)  # Ensure the target window is in focus
        keyboard_controller.press('s')  # Press and hold 'S'
        keyboard_controller.release('s')  # Release 'S'
        keyboard_controller.press(Key.enter)  # Press and hold 'Enter'
        keyboard_controller.release(Key.enter)  # Release 'Enter'
        time.sleep(spam_speed)
        
        # Fail-safe: Stop after 20 seconds
        if time.time() - start_time >= 20:
            print("Failsafe activated. Stopping spamming after 20 seconds.")
            stop_event.set()

# Function to handle toggle action (start/stop spamming)
def toggle_spamming(window_title):
    global spamming
    if spamming:
        # If spamming is active, stop it
        stop_event.set()  # Stop the current spamming thread
        spamming = False
    else:
        # If spamming is inactive, start it
        stop_event.clear()  # Reset the stop event
        threading.Thread(target=spam_keys, args=(window_title,), daemon=True).start()  # Start a new thread to spam keys
        spamming = True

# Function to listen for the F6 key press to toggle spamming
def on_press(key, window_title):
    try:
        if key == Key.f6:
            toggle_spamming(window_title)  # Toggle the spamming on F6 key press
    except AttributeError:
        pass

# Function to update the spam speed
def update_spam_speed():
    global spam_speed
    spam_speed = float(spam_speed_entry.get()) / 1000  # Convert milliseconds to seconds

# Set up the UI for the script
root = tk.Tk()
root.title("Auto Shake")

tk.Label(root, text="Window Title (Roblox):").grid(row=0, column=0)
window_title_entry = tk.Entry(root)
window_title_entry.grid(row=0, column=1)

tk.Label(root, text="Speed (milliseconds):").grid(row=1, column=0)
spam_speed_entry = tk.Entry(root)
spam_speed_entry.grid(row=1, column=1)
spam_speed_entry.insert(0, str(spam_speed * 1000))  # Display in milliseconds

tk.Button(root, text="Update Speed", command=update_spam_speed).grid(row=3, column=0, columnspan=2)

# Start the tkinter UI in the main thread
def start_listener():
    window_title = window_title_entry.get()  # Get the target window title from the entry
    listener = Listener(on_press=lambda key: on_press(key, window_title))
    listener.start()

# Create a button to start the listener
start_listener_button = tk.Button(root, text="Set Selected Window", command=start_listener)
start_listener_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
