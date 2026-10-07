# bring in tools for talking to OpenRouter over the internet
import json
import os
import urllib.request

# the address of OpenRouter, and a router that picks a free model for me
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"

# read my secret key from the environment variable, so it is never written in this file
API_KEY = os.environ.get("OPENROUTER_API_KEY")

# stop with a clear message if the key is missing
if API_KEY is None:
    raise SystemExit("No OPENROUTER_API_KEY found. Set it first.")

# this function sends a question to OpenRouter and returns its answer
def ask_openrouter(question):
    body = {"model": MODEL, "messages": [{"role": "user", "content": question}]}
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + API_KEY}
    request = urllib.request.Request(OPENROUTER_URL, data=data, headers=headers)
    with urllib.request.urlopen(request) as response:
        reply = json.loads(response.read().decode("utf-8"))
    return reply["choices"][0]["message"]["content"]

# try it: ask one question and print the answer
print(ask_openrouter("Say hello in one short sentence."))