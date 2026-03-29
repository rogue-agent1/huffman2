#!/usr/bin/env python3
"""huffman2: Huffman coding with serialization."""
import heapq, sys

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char; self.freq = freq; self.left = left; self.right = right
    def __lt__(self, other): return self.freq < other.freq

def build_tree(freq):
    heap = [Node(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, Node(freq=a.freq + b.freq, left=a, right=b))
    return heap[0] if heap else None

def build_codes(root):
    codes = {}
    def walk(node, prefix=""):
        if node.char is not None:
            codes[node.char] = prefix or "0"
            return
        if node.left: walk(node.left, prefix + "0")
        if node.right: walk(node.right, prefix + "1")
    if root: walk(root)
    return codes

def encode(text):
    freq = {}
    for c in text: freq[c] = freq.get(c, 0) + 1
    tree = build_tree(freq)
    codes = build_codes(tree)
    bits = "".join(codes[c] for c in text)
    # Pack to bytes
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding
    data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return data, codes, padding

def decode(data, codes, padding):
    reverse = {v: k for k, v in codes.items()}
    bits = "".join(f"{b:08b}" for b in data)
    if padding: bits = bits[:-padding]
    result = []
    current = ""
    for bit in bits:
        current += bit
        if current in reverse:
            result.append(reverse[current])
            current = ""
    return "".join(result)

def test():
    text = "hello world"
    data, codes, padding = encode(text)
    decoded = decode(data, codes, padding)
    assert decoded == text
    # Compression
    text2 = "aaaaaabbbbccdd"
    data2, codes2, pad2 = encode(text2)
    assert len(data2) < len(text2)
    assert decode(data2, codes2, pad2) == text2
    # Single char
    text3 = "aaaa"
    data3, codes3, pad3 = encode(text3)
    assert decode(data3, codes3, pad3) == text3
    # All unique
    text4 = "abcdefgh"
    data4, codes4, pad4 = encode(text4)
    assert decode(data4, codes4, pad4) == text4
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: huffman2.py test")
