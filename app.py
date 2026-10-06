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

# this function runs when I click Send or press Enter
def send_message(event=None):
    text = entry.get()
    chat.insert(tk.END, "You: " + text + "\n")
    chat.insert(tk.END, "AI: I received your message.\n\n")
    chat.see(tk.END)
    entry.delete(0, tk.END)

# pressing the Enter key also runs the function
entry.bind("<Return>", send_message)

# create the Send button and connect it to the function
button = tk.Button(root, text="Send", command=send_message)

# place the button in the window
button.pack()

# keep the window open and waiting for me
root.mainloop()