# bring in tkinter, python's tool for making windows
import tkinter as tk

# create the main window
root = tk.Tk()

# set the text at the top of the window
root.title("My AI App")

# set the window size: 600 wide, 400 tall
root.geometry("600x400")

# create the text label
label = tk.Label(root, text="Hello, I am your AI assistant")

# place the label inside the window
label.pack()

# keep the window open and waiting for me
root.mainloop()