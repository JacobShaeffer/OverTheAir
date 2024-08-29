import tkinter as tk
from tkinter import ttk
from upload import pack_transfer
from pack import pack
import re

def update_progress(value):
    """
    Update the progress bar to the specified value.
    :param value: int, value between 0 and 100 indicating progress percentage.
    """
    progress_bar['value'] = value
    root.update()  # Update the GUI to reflect the change

def upload_progress(message):
    """
    Extracts and prints the percentage from a given line of rsync output.
    :param message: str, a line of output from an rsync process
    """
    try:
        # Attempt to find a percentage value in the line using a regular expression
        match = re.search(r'(\d+)%', message)
        if match:
            # If a percentage is found, print it without the '%' sign
            val = match.group(1)
            print(val)
            update_progress(val)
        else:
            # If no percentage is found, handle unexpected formats or blank lines
            match(message):
                case 'database':
                    print("it's working")
                case _: #default case
                    print("No percentage found in line.")
    except Exception as e:
        # Handle any other kind of unexpected error
        print(f"Error processing the line: {str(e)}")


def progress(value):
    progress_bar['value'] = value
    root.update()

def on_button_click():
    """
    Simulate some updates to the progress bar.
    """
    # pack_location = "/Users/jacob/Documents/scratch/OverTheAir/test1.pack"
    # pack_transfer(pack_location, upload_progress)

    progress(50)

# Create the main window
root = tk.Tk()
root.title("Progress Bar Example")
root.geometry("300x100")  # Set the size of the window

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=20)  # Add some vertical padding

# Create a button that when clicked, will update the progress bar
button = ttk.Button(root, text="Start Progress", command=on_button_click)
button.pack(pady=10)

root.mainloop()
