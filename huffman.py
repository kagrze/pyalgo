import bitarray  # you need to install bitarray package, e.g. "sudo pip3 install bitarray"


class Node:
    def __init__(self, char=None, left=None, right=None):
        self.__char = char
        self.__left = left
        self.__right = right

    @property
    def char(self):
        return self.__char

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    @property
    def is_leaf(self):
        return self.__left is None and self.__right is None

    def __lt__(self, other):  # heapq requires this method, but it is not used
        return True


def compress(text_file_path, compressed_file_path):
    char_frequency_map = _build_char_frequency_map(text_file_path)

    trie = _build_trie(char_frequency_map)

    code_map = dict(_build_code_map(trie, []))

    bits = bitarray.bitarray()

    _serialize_trie(trie, bits)

    _serialize_file_size(text_file_path, bits)

    with open(text_file_path, 'r') as text_stream:
        _encode_text(code_map, text_stream, bits)

    with open(compressed_file_path, 'wb') as compressed_stream:
        bits.tofile(compressed_stream)


def _build_char_frequency_map(file_path):
    char_frequency_map = {}

    with open(file_path, 'r') as text_stream:
        while True:
            c = text_stream.read(1)
            if not c:
                break
            if c in char_frequency_map:
                char_frequency_map[c] += 1
            else:
                char_frequency_map[c] = 1
    return char_frequency_map


def _build_trie(char_frequency_map):
    from heapq import heappush, heappop

    nodes = []
    for c, f in char_frequency_map.items():
        heappush(nodes, (f, Node(char=c)))

    while len(nodes) > 1:
        f1, n1 = heappop(nodes)
        f2, n2 = heappop(nodes)
        heappush(nodes, (f1 + f2, Node(left=n1, right=n2)))
    return nodes.pop()[1]


def _build_code_map(node, code):
    from copy import copy

    if node.is_leaf:
        return [(node.char, code)]

    code_copy = copy(code)
    code.append(False)
    code_copy.append(True)

    code_map = []
    code_map.extend(_build_code_map(node.left, code))
    code_map.extend(_build_code_map(node.right, code_copy))
    return code_map


def _serialize_trie(trie, bits):
    if trie.is_leaf:
        bits.append(True)
        char_bits = bitarray.bitarray()
        char_bits.frombytes(trie.char.encode())
        bits.extend(char_bits)
    else:
        bits.append(False)
        _serialize_trie(trie.left, bits)
        _serialize_trie(trie.right, bits)


def _serialize_file_size(file_path, bits):
    file_size = os.path.getsize(file_path)
    file_size_bits = bin(file_size)[2:]
    for i in range(32 - len(file_size_bits)):
        bits.append(False)
    for bit_position in range(len(file_size_bits)):
        bits.append(file_size_bits[bit_position] == '1')


def _encode_text(code_map, text_stream, bits):
    while True:
        c = text_stream.read(1)
        if not c:
            break
        bits.extend(code_map[c])


def decompress(compressed_file_path, decompressed_file_path):
    from collections import deque

    bits = bitarray.bitarray()

    with open(compressed_file_path, 'rb') as compressed_stream:
        bits.fromfile(compressed_stream)

    bits_queue = deque(bits)

    trie = _deserialize_trie(bits_queue)

    file_size = _deserialize_file_size(bits_queue)

    with open(decompressed_file_path, 'w') as text_output_stream:
        _decode_text(trie, bits_queue, file_size, text_output_stream)


def _deserialize_trie(code):
    if code.popleft():
        char_as_bitarray = []
        for i in range(8):
            char_as_bitarray.append(code.popleft())
        return Node(char=bitarray.bitarray(char_as_bitarray).tostring())
    return Node(left=_deserialize_trie(code), right=_deserialize_trie(code))


def _deserialize_file_size(bits_queue):
    file_size = 0
    for bit_position in range(32):
        file_size = (file_size << 1) | bits_queue.popleft()
    return file_size


def _decode_text(trie, code, length, text_output_stream):
    for i in range(length):
        node = trie
        while not node.is_leaf:
            bit = code.popleft()
            node = node.right if bit else node.left
        text_output_stream.write(node.char)


if __name__ == '__main__':
    import os

    text_to_compress = 'aaaaaaaaaaaaaaa dmr zzzzzzzzzzzzzzzz'
    tmp_text_file = 'tmp1.txt'
    tmp_compressed_file = 'tmp.co'
    tmp_decompressed_file = 'tmp2.txt'

    with open(tmp_text_file, 'w') as txt_stream:
        txt_stream.write(text_to_compress)

    compress(tmp_text_file, tmp_compressed_file)

    decompress(tmp_compressed_file, tmp_decompressed_file)

    with open(tmp_decompressed_file, 'r') as txt_stream:
        assert text_to_compress == txt_stream.read()

    assert os.path.getsize(tmp_text_file) == os.path.getsize(tmp_decompressed_file)
    assert os.path.getsize(tmp_compressed_file) < os.path.getsize(tmp_text_file)

    os.remove(tmp_text_file)
    os.remove(tmp_compressed_file)
    os.remove(tmp_decompressed_file)

    print('All tests passed')
