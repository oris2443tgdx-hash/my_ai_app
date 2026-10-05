# tkinter is Python's built-in tool for making windows; "as tk" is a short name for it
import tkinter as tk

# create the main window and call it root
root = tk.Tk()
root.geometry("600x400")

# put the text "My AI App" at the top of the window
#root.title("My AI App")

# keep the window open and waiting for me
#label = tk.Label(root, text="Hello, I am your AI assistant")
#label.pack()
root.mainloop()