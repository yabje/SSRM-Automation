import time
import requests
from tkinter import *

def submit():

    global bsr
    bsr = str(mapKey_entry.get())

    # Print the map code to confirm it has been stored correctly
    print(f"The entered map key is: {bsr}")


    # Api call to beatsaver
    r = requests.get(f"https://api.beatsaver.com/maps/id/{bsr}")

    if r.status_code == 200:
        data = r.json()
        mapName = data['name']
    else:
        print(f"Failed to get map info for {bsr}. Status code: {r.status_code}")

    # Print the map name
    print(mapName)

    # Wait 10 seconds before closing
    time.sleep(10)


root = Tk()
root.title("SSRM Automator")
root.geometry('600x400')

mapKey_label = Label(root, text="Map key:")
mapKey_label.pack()
mapKey_entry = Entry(root)
mapKey_entry.pack()

submit_button = Button(root, text= "Submit", command=submit)
submit_button.pack()

# Print GUI
root.mainloop()