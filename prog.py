import requests
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Function to handle the submit button click event
def submit():
    global bsr
    bsr = str(mapKey_entry.get())  # Get the map key from the entry widget
    global overlayImageUrl

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
        overlayImageUrl = data['versions'][0]['coverURL']

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
        description_text.insert(END, f"https://beatsaver.com/maps/{bsr}\n\n")
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

# Function to open a file dialog and select an image from the PC
def select_image():
    global selected_image_path
    selected_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if selected_image_path:
        print(f"Selected image: {selected_image_path}")

# Function to overlay the URL image onto the selected image and save the result
def overlay_and_save_image():
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return
    
    try:
        # Load the selected image
        selected_image = Image.open(selected_image_path).convert('RGBA')

        # Download and load the overlay image
        response = requests.get(overlayImageUrl)
        overlay_image = Image.open(BytesIO(response.content)).convert('RGBA')

        # Resize overlay image to 50x50 pixels
        overlay_image = overlay_image.resize((50, 50), Image.ANTIALIAS)

        # Create a new image with an alpha channel for transparency
        combined_image = Image.new('RGBA', selected_image.size)
        combined_image.paste(selected_image, (0, 0))
        combined_image.paste(overlay_image, (0, 0), overlay_image)

        # Save the combined image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            combined_image.save(file_path)
            print(f"Combined image saved as: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to overlay and save image: {e}")

# Create the main window
root = Tk()
root.title("SSRM Automator")
root.geometry('600x500')

# Set Lato font
font_style = ("Lato", 11)
headerFont_style = ("Lato Black", 14)

# Create a style object
style = ttk.Style()
style.configure('TButton', font=font_style)  # Apply the Lato font to all TButtons

# Create and pack the label and entry widgets for map key input
mapKey_label = ttk.Label(root, text="Map key:", font=headerFont_style)
mapKey_label.pack(pady=10)

mapKey_entry = ttk.Entry(root, font=font_style)
mapKey_entry.pack(pady=10)

# Bind the Enter key press events to submit the map key
mapKey_entry.bind('<Return>', lambda event: submit())
mapKey_entry.bind('<KP_Enter>', lambda event: submit())

# Create and pack the submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Create and pack the text widget to display the title
title_label = ttk.Label(root, text="Title:", font=headerFont_style)
title_label.pack()

title_text = Text(root, height=1, wrap=WORD, font=font_style)
title_text.pack(pady=10, fill=BOTH, expand=True)
title_text.config(state=DISABLED)  # Make text box read-only

# Create and place the copy image button for title
copy_title_button = Button(root, text="Copy", cursor="hand2", command=copy_title)
copy_title_button.place(x=560, y=80)  # Initial position; will be adjusted

# Create a spacer frame
spacer = Frame(root, height=20)  # Spacer with height 40 pixels
spacer.pack(fill=X)

# Create and pack the text widget to display the description
description_label = ttk.Label(root, text="Description:", font=headerFont_style)
description_label.pack()

description_text = Text(root, height=5, wrap=WORD, font=font_style)
description_text.pack(pady=10, fill=BOTH, expand=True)
description_text.config(state=DISABLED)  # Make text box read-only

# Create and place the copy image button for description
copy_description_button = Button(root, text="Copy", cursor="hand2", command=copy_description)
copy_description_button.place(x=560, y=210)  # Initial position; will be adjusted

# Create and pack the select image button
select_image_button = ttk.Button(root, text="Select Image", command=select_image)
select_image_button.pack(pady=10)

# Create and pack the overlay and save image button
overlay_save_image_button = ttk.Button(root, text="Overlay and Save Image", command=overlay_and_save_image)
overlay_save_image_button.pack(pady=10)

# Bind the window resize event to adjust the position of the copy buttons
root.bind('<Configure>', adjust_copy_button_positions)

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main event loop
root.mainloop()
