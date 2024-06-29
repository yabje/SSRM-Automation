import requests
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

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

        # Update the title text box with the fetched data
        title_text.config(state=NORMAL)
        title_text.delete(1.0, END)  # Clear previous content
        title_text.insert(END, f"{mapName} | {songAuthorName} | {levelAuthorName} | Ex+")
        title_text.config(state=DISABLED)  # Make text box read-only

        # Update the description text box with the fetched data
        description_text.config(state=NORMAL)
        description_text.delete(1.0, END)  # Clear previous content
        description_text.insert(END, f"{mapName} by {songAuthorName}\n")
        description_text.insert(END, f"Mapped by {levelAuthorName}\n")
        description_text.insert(END, f"https://beatsaver.com/maps/{bsr}\n")
        description_text.insert(END, f"Gameplay by: Mr_bjo")
        description_text.config(state=DISABLED)  # Make text box read-only

    else:
        print(f"Failed to get map info for {bsr}. Status code: {r.status_code}")

# Function to copy title text to clipboard
def copy_title(event=None):
    root.clipboard_clear()
    root.clipboard_append(title_text.get(1.0, END).strip())
    print("Title copied to clipboard")

# Function to copy description text to clipboard
def copy_description(event=None):
    root.clipboard_clear()
    root.clipboard_append(description_text.get(1.0, END).strip())
    print("Description copied to clipboard")

# Function to handle the window close event
def on_closing():
    print("Program closed.")
    root.destroy()

# Function to adjust the position of the copy buttons
def adjust_copy_button_positions(event):
    x_pos = root.winfo_width() - 40  # 10 pixels from the right edge, considering the button width
    title_button_y_pos = title_text.winfo_y() - 30  # 30 pixels above the title text box
    description_button_y_pos = description_text.winfo_y() - 30  # 30 pixels above the description text box
    copy_title_button.place(x=x_pos, y=title_button_y_pos)
    copy_description_button.place(x=x_pos, y=description_button_y_pos)

# Create the main window
root = Tk()
root.title("SSRM Automator")
root.geometry('600x400')

# Create and pack the label and entry widgets for map key input
mapKey_label = ttk.Label(root, text="Map key:")
mapKey_label.pack(pady=10)

mapKey_entry = ttk.Entry(root)
mapKey_entry.pack(pady=10)

# Bind the Enter key press events to submit the map key
mapKey_entry.bind('<Return>', lambda event: submit())
mapKey_entry.bind('<KP_Enter>', lambda event: submit())

# Create and pack the submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Create and pack the text widget to display the title
title_text = Text(root, height=1, wrap=WORD)
title_text.pack(pady=10, fill=BOTH, expand=True)
title_text.config(state=DISABLED)  # Make text box read-only

# Load the copy image
copy_image_path = "Images/copy-icon.png"
copy_image = Image.open(copy_image_path)
copy_image = copy_image.resize((18, 18), Image.LANCZOS)  # Resizer
copy_image = ImageTk.PhotoImage(copy_image)

# Create and place the copy image button for title
copy_title_button = Label(root, image=copy_image, cursor="hand2")
copy_title_button.place(x=560, y=80)  # Initial position; will be adjusted

# Create a spacer frame
spacer = Frame(root, height=40)  # Spacer with height 40 pixels
spacer.pack(fill=X)

# Create and pack the text widget to display the description
description_text = Text(root, height=5, wrap=WORD)
description_text.pack(pady=10, fill=BOTH, expand=True)
description_text.config(state=DISABLED)  # Make text box read-only

# Create and place the copy image button for description
copy_description_button = Label(root, image=copy_image, cursor="hand2")
copy_description_button.place(x=560, y=210)  # Initial position; will be adjusted

# Bind the window resize event to adjust the position of the copy buttons
root.bind('<Configure>', adjust_copy_button_positions)

# Bind the copy buttons to their respective functions
copy_title_button.bind("<Button-1>", copy_title)
copy_description_button.bind("<Button-1>", copy_description)

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main event loop
root.mainloop()