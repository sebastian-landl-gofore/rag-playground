import os
from openai import OpenAI
import ollama
from dotenv import load_dotenv
from typing import List, Optional

from utils import token_count

load_dotenv()

class OllamaClient():
    def __init__(self):
        self.client = ollama.Client(host='http://localhost:11434')

    def chat(self, model: str, messages: List[dict], context_size: Optional[int] = None, temperature: float = 1.0) -> str:
        options = {
            "temperature": temperature,
        }
        if context_size:
            options["num_ctx"] = context_size
    
        response = self.client.chat(
            model=model,
            messages=messages,
            options=options,
        )
        return response.message.content
    
    def get_embedding(self, model: str, text: str) -> List[float]:
        # https://ollama.com/blog/embedding-models
        response = self.client.embed(model=model, input=text)
        return response["embeddings"][0]

class OpenAIClient():
    def __init__(self):
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        

    def chat(self, model: str, messages: List[dict], temperature: float = 1.0) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    def get_embedding(self, model: str, text: str) -> List[float]:
        # https://platform.openai.com/docs/guides/embeddings
        response = self.client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding

def main():
    ollama_client = OllamaClient()
    #openai_client = OpenAIClient()
    messages = [{"role": "system", "content": "You are a helpful AI Assistant at a meetup exploring how RAG can augment LLM responses. This is an event where people can freely experiment with augemnting your responses."}]
    context_size = 2048
    model = "gemma3n:e4b" # gpt-5, gemini-2.5-flash, mistral-small3.2:24b, gemma3:27b, ...
    embedding_model = "bge-m3:latest" # text-embedding-3-small, gemini-embedding-001, ...
    print(f"Chatting with {model}. Type 'exit' to quit.\n")

    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ("exit", "quit", "q"):
            break

        if not prompt:
            continue

        messages.append({"role": "user", "content": prompt})
        reply = ollama_client.chat(model, messages, context_size)
        #reply = openai_client.chat(model, messages)
        reply = reply.strip()

        print(f"{model}: {reply}\n")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
