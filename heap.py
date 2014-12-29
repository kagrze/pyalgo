class Heap:
    """
    A binary heap with an ability to decrease key for a given value
    """
    _elements = []
    _value2index = {}

    def push(self, key, value):
        self._elements.append((key, value))
        index = len(self._elements) - 1
        self._value2index[value] = index
        self._bubble_up(index)

    def pop(self):
        if not self._elements:
            return None
        head = self._elements[0]
        last = self._elements.pop()
        if self._elements:
            self._elements[0] = last
            self._value2index[last[1]] = 0
            self._bubble_down(0)
        del self._value2index[head[1]]
        return head

    def size(self):
        return len(self._elements)

    def decrease_key(self, key, value):
        """
        This method works only when all the values on the heap are unique
        """
        index = self._value2index[value]
        self._elements[index] = (key, value)
        self._bubble_up(index)

    def get_key(self, value):
        """
        This method works only when all the values on the heap are unique
        """
        return None if value not in self._value2index else self._elements[self._value2index[value]][0]

    def _bubble_up(self, index):
        """
        a.k.a. swim
        """
        parent = int(index / 2)  # floor - rounding down
        parent -= 1 if index % 2 == 0 else 0
        if parent >= 0 and self._elements[parent][0] > self._elements[index][0]:
            parent_value = self._elements[parent][1]
            child_value = self._elements[index][1]
            self._elements[parent], self._elements[index] = self._elements[index], self._elements[parent]
            self._value2index[parent_value], self._value2index[child_value] = self._value2index[child_value], self._value2index[parent_value]
            self._bubble_up(parent)

    def _bubble_down(self, index):
        """
        a.k.a. sink
        """
        left = 2 * index + 1
        right = left + 1
        if right >= len(self._elements):
            if left >= len(self._elements):
                return None
            else:
                smaller_child = left
        else:
            smaller_child = left if self._elements[left][0] < self._elements[right][0] else right
        if self._elements[index][0] > self._elements[smaller_child][0]:
            parent_value = self._elements[index][1]
            child_value = self._elements[smaller_child][1]
            self._elements[index], self._elements[smaller_child] = self._elements[smaller_child], self._elements[index]
            self._value2index[parent_value], self._value2index[child_value] = self._value2index[child_value], self._value2index[parent_value]
            self._bubble_down(smaller_child)


if __name__ == '__main__':
    h1 = Heap()

    h1.push(3, 'a')
    h1.push(4, 'b')
    h1.push(2, 'c')
    h1.push(1, 'd')
    h1.push(5, 'e')
    h1.push(6, 'f')
    h1.push(0, 'g')

    assert h1.pop() == (0, 'g')
    assert h1.pop() == (1, 'd')
    assert h1.pop() == (2, 'c')
    assert h1.pop() == (3, 'a')
    assert h1.pop() == (4, 'b')
    assert h1.pop() == (5, 'e')
    assert h1.pop() == (6, 'f')
    assert h1.pop() is None

    h2 = Heap()

    h2.push(3, 'a')
    h2.push(4, 'b')
    h2.push(5, 'c')

    h2.decrease_key(1, 'b')
    h2.decrease_key(0, 'a')
    h2.decrease_key(2, 'c')

    assert h2.pop() == (0, 'a')
    assert h2.pop() == (1, 'b')

    h2.push(6, 'd')
    h2.push(7, 'e')
    h2.push(8, 'f')

    h2.decrease_key(5, 'e')

    h2.push(9, 'g')

    assert h2.pop() == (2, 'c')
    assert h2.pop() == (5, 'e')
    assert h2.pop() == (6, 'd')
    assert h2.pop() == (8, 'f')
    assert h2.pop() == (9, 'g')

    assert h2.pop() is None

    print('All tests passed')
