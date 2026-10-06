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

# try it: ask one question and print the answer
print(ask_ollama("Say hello in one short sentence."))