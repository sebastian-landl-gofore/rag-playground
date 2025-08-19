from typing import List, Any
import json
import tiktoken

def token_count(text: str, encoding: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding)
    return len(encoding.encode(text))

def read_file_content(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()
    
def read_file_lines(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        return f.readlines()
    
def read_json(filepath: str) -> Any:
    with open(filepath, "r") as f:
        return json.load(f)
