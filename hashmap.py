class HashMap:
    """Bucket collisions are resolved using open addressing (linear probing)
    For simplicity let's assume that the size of this hash map is fixed"""

    def __init__(self, hash_function):
        self.__size = 100
        # in order linear probing to work you need at least one empty element in an array
        self.__elements = [(None, None)] * (self.__size + 1)
        self.__hash_function = hash_function

    def __probe(self, hash_code, key):
        """linear probing"""
        relative_hash_code = hash_code % self.__size
        current_key, _ = self.__elements[relative_hash_code]
        return relative_hash_code if current_key == key or current_key is None else self.__probe(hash_code + 1, key)

    def __rehash(self, relative_hash_code):
        entry = self.__elements[relative_hash_code]
        if entry != (None, None):
            self.__elements[relative_hash_code] = self.__rehash((relative_hash_code + 1) % self.__size)
        return entry

    def set_value(self, key, value):
        self.__elements[self.__probe(self.__hash_function(key), key)] = (key, value)

    def get_value(self, key):
        return self.__elements[self.__probe(self.__hash_function(key), key)][1]

    def delete(self, key):
        self.__rehash(self.__probe(self.__hash_function(key), key))


def hash_string(string):
    """Horner's approach to string hashing"""
    from functools import reduce
    return reduce(lambda x, y: 31 * x + ord(y), string, 0)


if __name__ == '__main__':
    hm = HashMap(hash_string)
    hm.set_value('k0', 1)
    hm.set_value('k4', 2)
    hm.set_value('k5', 3)
    hm.set_value('k2', 4)
    hm.set_value('k1', 5)
    hm.set_value('k3', 6)
    hm.set_value('k0', 0)

    assert hm.get_value('k0') == 0
    assert hm.get_value('k1') == 5
    assert hm.get_value('k2') == 4
    assert hm.get_value('k3') == 6
    assert hm.get_value('k4') == 2
    assert hm.get_value('k5') == 3
    assert hm.get_value('k6') is None

    hm.delete('k0')
    hm.delete('k1')
    hm.delete('k2')
    hm.delete('k3')
    hm.delete('k4')
    hm.delete('k5')

    assert hm.get_value('k0') is None
    assert hm.get_value('k1') is None
    assert hm.get_value('k2') is None
    assert hm.get_value('k3') is None
    assert hm.get_value('k4') is None
    assert hm.get_value('k5') is None

    print('All tests passed')
