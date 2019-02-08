class Element:
    value = None
    next_element = None

    def __init__(self, value, next_element):
        self.value = value
        self.next_element = next_element


class Stack:
    _top = None

    def __nonzero__(self):
        return True if self._top else False

    def push(self, value):
        self._top = Element(value, self._top)

    def pop(self):
        if not self._top:
            return None
        value = self._top.value
        self._top = self._top.next_element
        return value


class Queue(Stack):
    _back = None

    def enqueue(self, value):
        new_element = Element(value, None)
        if self._back:
            self._back.next_element = new_element
        self._back = new_element
        if not self._top:
            self._top = new_element

    def dequeue(self):
        return self.pop()


if __name__ == '__main__':
    s = Stack()
    s.push(5)
    s.push(3)
    s.push(-1)

    assert s.pop() == -1
    assert s.pop() == 3
    assert s.pop() == 5
    assert s.pop() is None

    s = Queue()
    s.enqueue(5)
    s.enqueue(7)
    s.enqueue(3)

    assert s.dequeue() == 5
    assert s.dequeue() == 7
    assert s.dequeue() == 3
    assert s.dequeue() is None

    print('All tests passed')
