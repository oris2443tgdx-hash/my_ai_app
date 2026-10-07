# bring in tkinter, python's tool for making windows
import tkinter as tk

# bring in tools for talking to Ollama over the local network
import json
import urllib.request

# bring in the tool for running work in a second thread
import threading

# the address of Ollama on my PC, and the model I have installed
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

# this list remembers the whole conversation
history = []

# this function sends the whole conversation to Ollama and returns its answer
def ask_ollama(messages):
    body = {"model": MODEL, "messages": messages, "stream": False}
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

# this function runs in the second thread and waits for the AI
def get_answer():
    try:
        reply = ask_ollama(history)
        history.append({"role": "assistant", "content": reply})
    except Exception as error:
        history.pop()
        reply = "Sorry, I could not get an answer. Is Ollama running? (" + str(error) + ")"
    root.after(0, show_reply, reply)

# this function shows the AI's answer in the chat area
def show_reply(reply):
    chat.config(state="normal")
    chat.insert(tk.END, "AI: " + reply + "\n\n")
    chat.see(tk.END)
    chat.config(state="disabled")
    button.config(state="normal", text="Send")

# this function runs when I click Send or press Enter
def send_message(event=None):
    if button["state"] == "disabled":
        return
    text = entry.get().strip()
    if text == "":
        return
    history.append({"role": "user", "content": text})
    chat.config(state="normal")
    chat.insert(tk.END, "You: " + text + "\n")
    chat.config(state="disabled")
    entry.delete(0, tk.END)
    button.config(state="disabled", text="Thinking...")
    threading.Thread(target=get_answer, daemon=True).start()

# pressing the Enter key also runs the function
entry.bind("<Return>", send_message)

# create the Send button and connect it to the function
button = tk.Button(root, text="Send", command=send_message)

# place the button in the window
button.pack()

# keep the window open and waiting for me
root.mainloop()