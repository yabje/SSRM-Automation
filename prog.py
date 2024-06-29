import time
import requests
from tkinter import *
from tkinter import ttk

# Function to handle the submit button click event
def submit():
    global bsr
    bsr = str(mapKey_entry.get())  # Get the map key from the entry widget

    # Print the map key to confirm it has been stored correctly
    print(f"The entered map key is: {bsr}")

    # Make an API call to BeatSaver
    r = requests.get(f"https://api.beatsaver.com/maps/id/{bsr}")

    # Check if the API call was successful
    if r.status_code == 200:
        data = r.json()
        mapName = data['metadata']['songName']
        songAuthorName = data['metadata']['songAuthorName']
        levelAuthorName = data['metadata']['levelAuthorName']

        # Update the text box with the fetched data
        result_text.config(state=NORMAL)
        result_text.delete(1.0, END)  # Clear previous content
        result_text.insert(END, f"{mapName} by {songAuthorName}\n")
        result_text.insert(END, f"Mapped by {levelAuthorName}\n")
        result_text.insert(END, f"https://beatsaver.com/maps/{bsr}\n")
        result_text.config(state=DISABLED)  # Make text box read-only
    else:
        print(f"Failed to get map info for {bsr}. Status code: {r.status_code}")

# Function to handle the window close event
def on_closing():
    print("Program closed.")
    root.destroy()

# Create the main window
root = Tk()
root.title("SSRM Automator")
root.geometry('600x400')

# Create and pack the label and entry widgets for map key input
mapKey_label = ttk.Label(root, text="Map key:")
mapKey_label.pack(pady=10)

mapKey_entry = ttk.Entry(root)
mapKey_entry.pack(pady=10)

# Create and pack the submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Create and pack the text widget to display fetched data
result_text = Text(root, height=10, wrap=WORD)
result_text.pack(pady=10, fill=BOTH, expand=True)
result_text.config(state=DISABLED)  # Make text box read-only

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main event loop
root.mainloop()