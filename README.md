\# Oris — Local-First AI Assistant



Oris is a lightweight, privacy-focused desktop AI assistant built in Python. Designed as a dual-engine application, it runs \*\*100% offline via local LLM inference (Ollama)\*\* for daily privacy-sensitive tasks, while offering \*\*cloud model fallback (OpenRouter)\*\* for high-accuracy reasoning and factual grounding.



\---



\## Key Features



\- \*\*Dual AI Engines:\*\* Switch seamlessly between local inference (`Llama 3.2:1b` via Ollama) and high-parameter cloud models (`Llama 3.3 70B` via OpenRouter).

\- \*\*Offline Voice Output (TTS):\*\* Native Windows SAPI text-to-speech integration with thread-safe COM handling and an on-screen audio toggle.

\- \*\*Privacy First:\*\* Local chat history and queries stay on your machine when using the Ollama provider.

\- \*\*Safety \& Behavioral Guardrails:\*\* Integrated system prompt rules preventing sycophancy, lazy code snippets, and hallucinated sources.

\- \*\*Time Grounding:\*\* Automatically grounds conversations with real-time date awareness.

\- \*\*Secure Key Management:\*\* Zero API key exposure—credentials are loaded dynamically from environment variables and protected via `.gitignore`.

\- \*\*Responsive GUI:\*\* Native Tkinter interface running model queries in background threads to maintain continuous UI responsiveness.



\---



\## Technical Stack



| Component | Technology / Library |

| :--- | :--- |

| \*\*Language\*\* | Python 3.12+ |

| \*\*GUI Framework\*\* | Tkinter / ttk |

| \*\*Local Inference Engine\*\* | Ollama API (`localhost:11434`) |

| \*\*Cloud Provider\*\* | OpenRouter REST API |

| \*\*Text-to-Speech\*\* | Windows SAPI (`win32com.client` / `pythoncom`) |

| \*\*Security \& Env\*\* | Custom environment variable loader / `.env` |



\---



\## Project Structure



```text

my\_ai\_app/

├── app.py           # Main application loop, GUI, threading, and dual-provider routing

├── setkey.py        # Secure API key loader GUI tool

├── .gitignore       # Excludes sensitive environment files and caches

└── README.md        # Technical project documentation

