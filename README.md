### Summary
- autosave.py
  Auto Save files or live update files while working in another app like Arduino IDE, LTSpice, or AutoCAD. Useful for apps that lack autosave feature or where you frequently lose work without control of frequency of saves.

### Install executable
```sh
# Install python dependencies
pip install -r requirements.txt

# Install single file executable
pyinstaller autosave.spec

# OR
pyinstaller --one-file --windowed autosave.py --name autosave
```

### Example
```bash
python autosave.py /path/to/your/file.txt /path/to/backup/
```
This will create a backup of `file.txt` in the specified backup location wether directory `/backup_files` or file name `/backup.txt`. If no backup location is provided, it will create a backup in the same directory as the original file, with the name `file_backup.txt`.

If you generated an executable open your `\dist` folder in terminal and run
```bash
autosave /path/to/your/file.txt /path/to/backup/
```

It is recommended to add all scripts to a folder like `~\Scripts` and add that folder to your system environment variable if you would like to execute the script for any terminal on your device or create a shortcut to the folder and add it to your desktop. 