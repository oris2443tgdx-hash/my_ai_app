# bring in tkinter, python's tool for making windows
import tkinter as tk

# bring in tools for talking to Ollama over the local network
import json
import urllib.request

# the address of Ollama on my PC, and the model I have installed
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

# this function sends a question to Ollama and returns its answer
def ask_ollama(question):
    body = {"model": MODEL, "messages": [{"role": "user", "content": question}], "stream": False}
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.loads(response.read().decode("utf-8"))
    return reply["message"]["content"]

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

# lock the chat area so I cannot type in it by mistake
chat.config(state="disabled")

# create the text box where I type my message
entry = tk.Entry(root, width=50)

# place the text box in the window
entry.pack()

# this function runs when I click Send or press Enter
def send_message(event=None):
    text = entry.get().strip()
    if text == "":
        return
    chat.config(state="normal")
    chat.insert(tk.END, "You: " + text + "\n")
    reply = ask_ollama(text)
    chat.insert(tk.END, "AI: " + reply + "\n\n")
    chat.see(tk.END)
    chat.config(state="disabled")
    entry.delete(0, tk.END)

# pressing the Enter key also runs the function
entry.bind("<Return>", send_message)

# create the Send button and connect it to the function
button = tk.Button(root, text="Send", command=send_message)

# place the button in the window
button.pack()

# keep the window open and waiting for me
root.mainloop()