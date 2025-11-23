from typing import List

def chunk_text_by_sentences(text: str, max_chars: int = 1000) -> List[str]:
    """
    Simple chunker that tries to keep sentences whole and limited by max_chars.
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    cur = []
    cur_len = 0
    for s in sentences:
        if cur_len + len(s) > max_chars and cur:
            chunks.append(" ".join(cur))
            cur = [s]
            cur_len = len(s)
        else:
            cur.append(s)
            cur_len += len(s)
    if cur:
        chunks.append(" ".join(cur))
    return chunks
