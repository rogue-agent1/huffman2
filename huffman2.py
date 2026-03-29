#!/usr/bin/env python3
"""huffman2 - Huffman coding with tree serialization and compression ratio."""
import sys, heapq
from collections import Counter

class HuffNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char, self.freq = char, freq
        self.left, self.right = left, right
    def __lt__(self, o): return self.freq < o.freq

def build_tree(freq):
    heap = [HuffNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, HuffNode(freq=a.freq + b.freq, left=a, right=b))
    return heap[0] if heap else None

def build_codes(root):
    codes = {}
    def walk(node, prefix):
        if node.char is not None:
            codes[node.char] = prefix or "0"
            return
        if node.left: walk(node.left, prefix + "0")
        if node.right: walk(node.right, prefix + "1")
    if root: walk(root, "")
    return codes

def encode(text):
    freq = Counter(text)
    tree = build_tree(freq)
    codes = build_codes(tree)
    bits = "".join(codes[c] for c in text)
    return bits, codes, freq

def decode(bits, codes):
    rev = {v: k for k, v in codes.items()}
    result = []
    buf = ""
    for b in bits:
        buf += b
        if buf in rev:
            result.append(rev[buf])
            buf = ""
    return "".join(result)

def test():
    text = "aabbbccccdddddd"
    bits, codes, freq = encode(text)
    assert decode(bits, codes) == text
    assert len(codes["d"]) <= len(codes["a"])  # more frequent = shorter
    ratio = len(bits) / (len(text) * 8)
    assert ratio < 1.0
    # Single char
    b2, c2, _ = encode("aaaa")
    assert decode(b2, c2) == "aaaa"
    print("huffman2: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: huffman2.py --test")
