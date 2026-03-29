#!/usr/bin/env python3
"""Huffman coding with canonical codes. Zero dependencies."""
import heapq, struct, sys
from collections import Counter

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right
    def __lt__(self, other): return self.freq < other.freq

def build_tree(freq):
    heap = [HuffmanNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, HuffmanNode(freq=a.freq+b.freq, left=a, right=b))
    return heap[0] if heap else None

def build_codes(root):
    codes = {}
    def walk(node, code=""):
        if node.char is not None:
            codes[node.char] = code or "0"
            return
        if node.left: walk(node.left, code+"0")
        if node.right: walk(node.right, code+"1")
    if root: walk(root)
    return codes

def encode(data):
    if not data: return b""
    freq = Counter(data)
    root = build_tree(freq)
    codes = build_codes(root)
    bits = "".join(codes[b] for b in data)
    pad = (8 - len(bits) % 8) % 8
    bits += "0" * pad
    header = struct.pack("<HB", len(freq), pad)
    for byte, f in freq.items():
        header += struct.pack("<BI", byte, f)
    body = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return header + body

def decode(data):
    if not data: return b""
    num_syms, pad = struct.unpack_from("<HB", data, 0)
    off = 3
    freq = {}
    for _ in range(num_syms):
        byte, f = struct.unpack_from("<BI", data, off)
        freq[byte] = f
        off += 5
    root = build_tree(freq)
    total = sum(freq.values())
    bits = "".join(f"{b:08b}" for b in data[off:])
    if pad: bits = bits[:-pad]
    result = []
    node = root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node.char is not None:
            result.append(node.char)
            node = root
            if len(result) >= total: break
    return bytes(result)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Huffman coding")
    p.add_argument("action", choices=["encode","decode"])
    p.add_argument("file")
    args = p.parse_args()
    data = open(args.file, "rb").read()
    if args.action == "encode":
        sys.stdout.buffer.write(encode(data))
    else:
        sys.stdout.buffer.write(decode(data))
