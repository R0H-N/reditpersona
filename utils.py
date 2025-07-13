import tiktoken

def chunk_text(text, max_tokens=3000):
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    words = text.split("\n\n")
    chunks, current_chunk = [], ""
    
    for w in words:
        test_chunk = current_chunk + "\n\n" + w
        token_count = len(enc.encode(test_chunk))
        if token_count > max_tokens:
            chunks.append(current_chunk.strip())
            current_chunk = w
        else:
            current_chunk = test_chunk

    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks
