# Setup Instructions

## 1) Clone or Prepare the Repo
```bash
git clone https://github.com/sebastian-landl-gofore/rag-playground.git
```

## 2) Install dependencies
```bash
cd <your-cloned-repo-directory>
```

### Environment Setup

#### Recommended Fast Track (anaconda)

Install miniconda (recommended) or [anaconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions),

e.g. homebrew/mac
```bash
brew install --cask miniconda
```

```bash
conda create -n rag-playground python=3.12
conda init <bash/zsh/...(your shell)>
# You may also need to source your .<your shell>rc: source .<your shell>rc
conda activate rag-playground
```
### Alternatively, set up manually

### Install python 3 (3.12 recommended)

https://www.python.org/downloads/

### set up venv
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### Finally the actual dependency installation
```bash
pip install -r requirements.txt
```

## 3) Ollama (Local Option)

1. Install Ollama and run
   * **macOS**:

     ```bash
     brew install ollama
     ```
   * **Linux/Windows/macOS**: Use the [installer from Ollama’s website](https://ollama.com/download)

2. Run the local ollama server (if not started automatically by the installer):
   ```bash
     ollama serve
     ```

2. Pull a model:
   ```bash
   ollama pull gemma3n:e4b
   ```

   What model should I pull?
   Models come in different sizes. The bigger they are the more RAM (or VRAM) they need and they often also require more compute. Models have a name and size which in the ollama context is specified like this: _name:size_. A small starting point could be [gemma3n:e4b](https://ollama.com/library/gemma3n). If you have more (or less) power to spare, you may try an appropriately sized version of [gemma3](https://ollama.com/library/gemma3) or [mistral-small:24b](https://ollama.com/library/mistral-small3.2). Regarding size: you need to have enough memory to accomodate the model itself and you need some reserves for the context on top. Ultimately this depends on the context size you specify, but calculate a couple of GB to get started.

   If you go the local ollama route, best also pull an embedding model (we'll get to that):
   ```bash
   ollama pull bge-m3:latest
   ```

   If you want smaller models some options are:
   ```bash
   ollama pull gemma3:4b
   ```
   and for embeddings:
   ```bash
   ollama pull nomic-embed-text
   ```

3. List pulled models:
   ```bash
   ollama list
   ```

3. Have a quick chat:
   ```bash
   ollama run gemma3n:e4b
   ```

## 4) OpenAI‑Compatible API (Cloud Option)

An alternative to local: use any **OpenAI‑compatible endpoint**, such as **OpenAI**, **Gemini** (notably offers a [generous free tier](https://ai.google.dev/gemini-api/docs/rate-limits)) or **OpenRouter**.

Create a `.env` file in the project folder:

```env
OPENAI_API_KEY=sk-...
# Optionally, if using Gemini or another non-openai endpoint:
# OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

## 5) Run it
Configure your client and model in the `main.py` in the code and run it:
```bash
python main.py
```
