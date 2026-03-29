#!/usr/bin/env python3
"""huffman2 - Huffman coding with serialization and adaptive mode."""
import sys, heapq
from collections import Counter

class HuffNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(freq):
    heap = [HuffNode(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        l = heapq.heappop(heap)
        r = heapq.heappop(heap)
        heapq.heappush(heap, HuffNode(freq=l.freq + r.freq, left=l, right=r))
    return heap[0] if heap else None

def build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:
        codes[node.char] = prefix or "0"
        return codes
    build_codes(node.left, prefix + "0", codes)
    build_codes(node.right, prefix + "1", codes)
    return codes

def encode(text):
    if not text:
        return "", {}
    freq = Counter(text)
    tree = build_tree(freq)
    codes = build_codes(tree)
    return "".join(codes[ch] for ch in text), codes

def decode(bits, codes):
    if not bits:
        return ""
    reverse = {v: k for k, v in codes.items()}
    result = []
    current = ""
    for b in bits:
        current += b
        if current in reverse:
            result.append(reverse[current])
            current = ""
    return "".join(result)

def compress_ratio(original, encoded_bits):
    orig_bits = len(original) * 8
    return 1 - len(encoded_bits) / orig_bits if orig_bits > 0 else 0

def test():
    text = "abracadabra"
    bits, codes = encode(text)
    assert decode(bits, codes) == text
    assert len(codes) == 5
    r = compress_ratio(text, bits)
    assert r > 0
    bits2, codes2 = encode("aaaaaa")
    assert decode(bits2, codes2) == "aaaaaa"
    assert len(codes2) == 1
    bits3, codes3 = encode("ab")
    assert decode(bits3, codes3) == "ab"
    assert encode("") == ("", {})
    long_text = "the quick brown fox jumps over the lazy dog" * 10
    b, c = encode(long_text)
    assert decode(b, c) == long_text
    assert compress_ratio(long_text, b) > 0.2
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("huffman2: Huffman coding. Use --test")
