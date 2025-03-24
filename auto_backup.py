import threading
import time
from pathlib import Path
import os
import keyboard
import argparse

print("Auto Backup File")
print("Press Ctrl+Z or Esc to exit the program")

# check user OS support
if os.name == 'nt':
    profile = os.getenv('USERPROFILE')
elif os.name == 'posix':
    profile = os.getenv('HOME')
else:
    print("OS not supported")
    exit()

stop_event = threading.Event()
def listen_for_exit():
    try:
        while True:
            if keyboard.is_pressed('ctrl+z') or keyboard.is_pressed('esc'):  # Ctrl+Z or Esc
                print("Exiting program")
                stop_event.set()
                break
            time.sleep(0.1)
    except Exception as e:
        print(e)

try:
    threading.Thread(target=listen_for_exit, daemon=True).start()
except Exception as e:
    print(e)
    print("Error in threading")
    pass
    
# Use argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Auto Backup File")
parser.add_argument("input_path", help="Path to the file to backup")
parser.add_argument("save_path", nargs='?', default=None, help="Path to save the backup (optional)")
parser.add_argument("-t", "--time", type=float, default=3, help="Time interval in seconds (default: 3)")
parser.add_argument("-ms", "--milliseconds", type=float, default=None, help="Time interval in milliseconds (overrides -t)")

args = parser.parse_args()

# Use Path to process input and display paths to the user

# Check if the input path is a valid file
if not Path(args.input_path).is_file():
    print("The specified file does not exist.")
    exit()
else:
    input_path = Path(args.input_path)

print(f"File location provided: {Path(input_path)}")

# Set the save path if not provided
if not args.save_path:
    save_path = input_path.parent / (input_path.stem + "_backup" + input_path.suffix)
else:
    save_path = Path(save_path)

print(f"Saving file at: {save_path}")

def copy_file():
    global input_path, save_path  # Add this line to access the global variable
    while not stop_event.is_set():
        try:
            with open(input_path, 'rb') as src:
                filedata = src.read()
                if save_path.is_dir():
                    save_path = save_path / input_path.name
                with open(save_path, 'wb') as file:
                    file.write(filedata)
            print(". ", end="\n") # Saved successfully
            if args.milliseconds:
                time.sleep(args.milliseconds / 1000)  # Convert milliseconds to seconds
            else:
                time.sleep(args.time)
        except Exception as e:
            print(e)
            time.sleep(3)

try: 
    threading.Thread(target=copy_file, daemon=True).start()
    while not stop_event.is_set():
        time.sleep(1)  # Keep the main thread alive
except Exception as e:
    print(e)
    print("Error in threading")
    pass