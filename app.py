# bring in tkinter, python's tool for making windows
import tkinter as tk
# bring in tools for talking to Ollama over the local network
import json
import urllib.request
# bring in tools for running work in background threads
import threading
# bring in tools for Windows offline text-to-speech
import win32com.client
import pythoncom
# bring in tool for reading today's date
import datetime

# the address of Ollama on my PC, and the model I have installed
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

# the name of my bot
BOT_NAME = "Oris"

# today's date written in words
TODAY = datetime.date.today().strftime("%A, %d %B %Y")

# note shown at bottom about privacy
PRIVACY_NOTE = "Privacy: Ollama runs on this PC, so your messages stay on this PC."

# rules shaping bot behavior
RULES = [
    "Never agree with something that is false. Politely say it is wrong and give the correct answer.",
    "Be honest. If you do not know, say so. Never invent facts, links, names or sources.",
    "If the user is upset with your answer, say sorry once, then ask what was missing or try again.",
    "Write in plain, simple English without fancy filler words, and keep answers short.",
    "The user may make spelling mistakes. Work out what they meant and do not point the mistakes out.",
    "When asked for code, give the complete code without leaving placeholders.",
    "If you cannot help, say so kindly in one sentence and suggest what you can do.",
]

# build the system prompt
SYSTEM_PROMPT = "Your name is " + BOT_NAME + ". Today's date is " + TODAY + ". You are a friendly, helpful AI assistant. Follow these rules: " + " ".join(RULES)

# example conversation history
EXAMPLES = [
    {"role": "user", "content": "The capital of France is Berlin, right?"},
    {"role": "assistant", "content": "No, the capital of France is Paris."},
    {"role": "user", "content": "That answer is useless."},
    {"role": "assistant", "content": "Sorry about that. Can you tell me what was missing? I will try again."},
    {"role": "user", "content": "Who won the 2060 football tournament?"},
    {"role": "assistant", "content": "I do not know. That tournament has not happened yet."},
]

STARTING_MESSAGES = [{"role": "system", "content": SYSTEM_PROMPT}] + EXAMPLES
history = list(STARTING_MESSAGES)

def ask_ollama(messages):
    body = {"model": MODEL, "messages": messages, "stream": False}
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request) as response:
        reply = json.loads(response.read().decode("utf-8"))
    return reply["message"]["content"]

def speak_text(text):
    if speak_var.get() == 1:
        try:
            # initialize COM library on this background thread
            pythoncom.CoInitialize()
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except Exception:
            pass

# create main window
root = tk.Tk()
root.title(BOT_NAME + " - AI Assistant")
root.geometry("600x530")

label = tk.Label(root, text="Hello, I am " + BOT_NAME + ", your AI assistant")
label.pack()

chat_frame = tk.Frame(root)
chat_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side="right", fill="y")

chat = tk.Text(chat_frame, height=12, width=70, wrap="word", yscrollcommand=scrollbar.set)
chat.pack(side="left", fill="both", expand=True)
scrollbar.config(command=chat.yview)
chat.config(state="disabled")

# Voice toggle checkbox
speak_var = tk.IntVar(value=1)
speak_check = tk.Checkbutton(root, text="Speak answers out loud", variable=speak_var)
speak_check.pack()

entry = tk.Entry(root, width=50)
entry.pack()

def get_answer():
    try:
        reply = ask_ollama(history)
        history.append({"role": "assistant", "content": reply})
    except Exception as error:
        history.pop()
        reply = "Sorry, I could not get an answer. Is Ollama running? (" + str(error) + ")"
    root.after(0, show_reply, reply)

def show_reply(reply):
    chat.config(state="normal")
    chat.insert(tk.END, BOT_NAME + ": " + reply + "\n\n")
    chat.see(tk.END)
    chat.config(state="disabled")
    button.config(state="normal", text="Send")
    
    # speak reply in background thread
    if speak_var.get() == 1:
        threading.Thread(target=speak_text, args=(reply,), daemon=True).start()

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

def clear_chat():
    if button["state"] == "disabled":
        return
    history.clear()
    history.extend(STARTING_MESSAGES)
    chat.config(state="normal")
    chat.delete("1.0", tk.END)
    chat.config(state="disabled")

entry.bind("<Return>", send_message)

button = tk.Button(root, text="Send", command=send_message)
button.pack()

clear_button = tk.Button(root, text="Clear chat", command=clear_chat)
clear_button.pack()

privacy = tk.Label(root, text=PRIVACY_NOTE, fg="gray")
privacy.pack()

root.mainloop()