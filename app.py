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

# create the chat area where messages will show
chat = tk.Text(root, height=12, width=70)

# place the chat area in the window
chat.pack()

# create the text box where I type my message
entry = tk.Entry(root, width=50)

# place the text box in the window
entry.pack()

# this function runs every time the Send button is clicked
def send_message():
    text = entry.get()
    chat.insert(tk.END, "You: " + text + "\n")
    entry.delete(0, tk.END)

# create the Send button and connect it to the function
button = tk.Button(root, text="Send", command=send_message)

# place the button in the window
button.pack()

# keep the window open and waiting for me
root.mainloop()