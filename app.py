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

# the name of my bot
BOT_NAME = "Oris"

# the rules that shape how the bot talks; the user never sees them
RULES = [
    "Never agree with something that is false. Politely say it is wrong and give the correct answer.",
    "Be honest. If you do not know, say so. Never invent facts, links, names or sources.",
    "If the user is upset with your answer, say sorry once, then ask what was missing or try again.",
    "Write in plain, simple English without fancy filler words, and keep answers short.",
    "The user may make spelling mistakes. Work out what they meant and do not point the mistakes out.",
    "When asked for code, give the complete code.",
    "If you cannot help, say so kindly in one sentence and suggest what you can do.",
]

# build the hidden instruction from the name and the rules
SYSTEM_PROMPT = "Your name is " + BOT_NAME + ". You are a friendly, helpful AI assistant. Follow these rules: " + " ".join(RULES)

# example conversations that show Oris how to behave; the user never sees them
EXAMPLES = [
    {"role": "user", "content": "The capital of France is Berlin, right?"},
    {"role": "assistant", "content": "No, the capital of France is Paris."},
    {"role": "user", "content": "That answer is useless."},
    {"role": "assistant", "content": "Sorry about that. Can you tell me what was missing? I will try again."},
    {"role": "user", "content": "Who won the 2060 football tournament?"},
    {"role": "assistant", "content": "I do not know. That tournament has not happened yet."},
]

# this list remembers the whole conversation, starting with the hidden instruction and the examples
history = [{"role": "system", "content": SYSTEM_PROMPT}] + EXAMPLES

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
root.title(BOT_NAME + " - AI Assistant")

# set the window size: 600 wide, 400 tall
root.geometry("600x400")

# create the text label
label = tk.Label(root, text="Hello, I am " + BOT_NAME + ", your AI assistant")

# place the label inside the window
label.pack()

# create a frame, an invisible box that holds the chat area and its scrollbar
chat_frame = tk.Frame(root)

# place the frame in the window and let it stretch with the window
chat_frame.pack(fill="both", expand=True)

# create the scrollbar inside the frame
scrollbar = tk.Scrollbar(chat_frame)

# place the scrollbar on the right side of the frame
scrollbar.pack(side="right", fill="y")

# create the chat area inside the frame and connect it to the scrollbar
chat = tk.Text(chat_frame, height=12, width=70, wrap="word", yscrollcommand=scrollbar.set)

# place the chat area on the left side of the frame
chat.pack(side="left", fill="both", expand=True)

# connect the scrollbar back to the chat area
scrollbar.config(command=chat.yview)

# lock the chat area so I cannot type in it by mistake
chat.config(state="disabled")

# create the text box where the user types a message
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

# this function shows the bot's answer in the chat area
def show_reply(reply):
    chat.config(state="normal")
    chat.insert(tk.END, BOT_NAME + ": " + reply + "\n\n")
    chat.see(tk.END)
    chat.config(state="disabled")
    button.config(state="normal", text="Send")

# this function runs when the user clicks Send or presses Enter
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
    button.config(state="disabled", text=BOT_NAME + " is replying...")
    threading.Thread(target=get_answer, daemon=True).start()

# pressing the Enter key also runs the function
entry.bind("<Return>", send_message)

# create the Send button and connect it to the function
button = tk.Button(root, text="Send", command=send_message)

# place the button in the window
button.pack()

# keep the window open and waiting for the user
root.mainloop()