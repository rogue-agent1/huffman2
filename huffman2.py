#!/usr/bin/env python3
"""Huffman coding — build tree, encode, decode."""
import sys, heapq
from collections import Counter

class HuffNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right
    def __lt__(self, other): return self.freq < other.freq

def build_tree(text):
    freq = Counter(text)
    heap = [HuffNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, HuffNode(freq=a.freq+b.freq, left=a, right=b))
    return heap[0] if heap else None

def build_codes(root):
    codes = {}
    def traverse(node, code):
        if node.char is not None:
            codes[node.char] = code or "0"
            return
        if node.left: traverse(node.left, code + "0")
        if node.right: traverse(node.right, code + "1")
    if root: traverse(root, "")
    return codes

def encode(text):
    tree = build_tree(text)
    codes = build_codes(tree)
    bits = "".join(codes[c] for c in text)
    return bits, tree, codes

def decode(bits, tree):
    if not tree: return ""
    if tree.char is not None: return tree.char * len(bits)
    result = []
    node = tree
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.char is not None:
            result.append(node.char)
            node = tree
    return "".join(result)

def test():
    text = "abracadabra"
    bits, tree, codes = encode(text)
    decoded = decode(bits, tree)
    assert decoded == text
    assert len(bits) < len(text) * 8  # compressed
    assert len(codes) == len(set(text))
    # Single char
    bits2, tree2, _ = encode("aaaa")
    assert decode(bits2, tree2) == "aaaa"
    print("  huffman2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Huffman coding")
