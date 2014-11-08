class Heap:
    elements = []

    def insert(self, element):
        self.elements.append(element)
        self.bubble_up(len(self.elements) - 1)

    def bubble_up(self, index):
        parent = int(index / 2)  # floor - rounding down
        parent -= 1 if index % 2 == 0 else 0
        if parent >= 0 and self.elements[parent] > self.elements[index]:
            self.elements[parent], self.elements[index] = self.elements[index], self.elements[parent]
            self.bubble_up(parent)

    def poll(self):
        if not self.elements:
            return None
        head = self.elements[0]
        last = self.elements.pop()
        if self.elements:
            self.elements[0] = last
            self.bubble_down(0)
        return head

    def bubble_down(self, index):
        left = 2 * index + 1
        right = left + 1
        if right >= len(self.elements):
            if left >= len(self.elements):
                return None
            else:
                smaller_child = left
        else:
            smaller_child = left if self.elements[left] < self.elements[right] else right
        if self.elements[index] > self.elements[smaller_child]:
            self.elements[index], self.elements[smaller_child] = self.elements[smaller_child], self.elements[index]
            self.bubble_down(smaller_child)

if __name__ == '__main__':
    h = Heap()

    h.insert(3)
    h.insert(4)
    h.insert(2)
    h.insert(1)
    h.insert(5)
    h.insert(6)
    h.insert(0)

    assert h.poll() == 0
    assert h.poll() == 1
    assert h.poll() == 2
    assert h.poll() == 3
    assert h.poll() == 4
    assert h.poll() == 5
    assert h.poll() == 6
    assert h.poll() is None

    print('All tests passed')
