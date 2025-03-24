import threading
import time
from pathlib import Path
import os
import sys
import keyboard 

print("Auto Backup File")
print("Press Ctrl+Z or Esc to exit the program")

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

if (len(sys.argv) == 0) or (len(sys.argv) > 3):
    print("Usage: python auto_backup.py <file_path> <save_path> invalid number of arguments")
    exit()

input_path = sys.argv[1]
print(f"File location provided: {input_path}")

input_path = Path(input_path)
save_path = input_path.parent / (input_path.stem + "_backup" + input_path.suffix)

if len(sys.argv) == 3:
    save_path = sys.argv[2]
    save_path = Path(save_path)
    print(f"Saving file at: {save_path}")

if os.name == 'nt':
    profile = os.getenv('USERPROFILE')
elif os.name == 'posix':
    profile = os.getenv('HOME')
else:
    print("OS not supported")
    exit()

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
            time.sleep(1)
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