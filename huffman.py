import heapq #Create priority queue
from collections import defaultdict, Counter #count char freq
import pickle 

#Rep nodes
class Node:
    def __init__(self, char, freq):
        self.char = char #a,b....
        self.freq = freq #freq of char
        self.left = None #child
        self.right = None 

    #lets heapq sort by freq
    def __lt__(self, other):
        return self.freq < other.freq

#build huffman tree
def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]

#assign 0,1 
def build_codes(node, prefix='', code_map=None):
    if code_map is None:
        code_map = {}
    if node.char is not None:
        code_map[node.char] = prefix
    else:
        build_codes(node.left, prefix + '0', code_map)
        build_codes(node.right, prefix + '1', code_map)
    return code_map

#encoded text
def huffman_compress(text):
    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded_text = ''.join(codes[ch] for ch in text)

    # Save both the encoded text and the code map
    return encoded_text, codes
#saving huffman text
def compress_to_file(text, filepath):
    encoded_text, code_map = huffman_compress(text)
    with open(filepath, 'wb') as f:
        pickle.dump((encoded_text, code_map), f)

#decompress text
def huffman_decompress(filepath):
    with open(filepath, 'rb') as f:
        encoded_text, code_map = pickle.load(f)

    # Reverse the code map
    reverse_map = {v: k for k, v in code_map.items()}

    # Decode the binary string
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_map:
            decoded_text += reverse_map[current_code]
            current_code = ""

    return decoded_text

def huffman_compress(text):
    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded = ''.join(codes[ch] for ch in text)
    return encoded, codes

def huffman_decode(encoded_text, code_map):
    reverse = {v: k for k, v in code_map.items()}
    current_code = ""
    decoded = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse:
            decoded += reverse[current_code]
            current_code = ""
    return decoded

