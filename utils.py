import tiktoken

def token_count(text: str, encoding: str = "cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding)
    return len(encoding.encode(text))
