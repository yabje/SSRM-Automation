import time
import requests
from tkinter import *
from tkinter import ttk

def submit():
    global bsr
    bsr = str(mapKey_entry.get())

    # Print the map code to confirm it has been stored correctly
    print(f"The entered map key is: {bsr}")

    # Api call to beatsaver
    r = requests.get(f"https://api.beatsaver.com/maps/id/{bsr}")

    if r.status_code == 200:
        data = r.json()
        mapName = data['metadata']['songName']
        songAuthorName = data['metadata']['songAuthorName']
        levelAuthorName = data['metadata']['levelAuthorName']
    else:
        print(f"Failed to get map info for {bsr}. Status code: {r.status_code}")

    # Print the map name
    print()
    print(f"{mapName} by {songAuthorName}")
    print(f"Mapped by {levelAuthorName}")
    print(f"https://beatsaver.com/maps/{bsr}")

def on_closing():
    print("Program closed.")
    root.destroy()

root = Tk()
root.title("SSRM Automator")
root.geometry('600x400')

mapKey_label = ttk.Label(root, text="Map key:")
mapKey_label.pack(pady=10)

mapKey_entry = ttk.Entry(root)
mapKey_entry.pack(pady=10)

submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Print GUI
root.mainloop()