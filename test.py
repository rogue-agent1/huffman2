from huffman2 import encode, decode
data = b"ABRACADABRA"
enc = encode(data)
dec = decode(enc)
assert dec == data, f"Got {dec}"
assert len(enc) < len(data) * 2
assert encode(b"") == b""
print("Huffman tests passed")