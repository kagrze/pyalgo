class Element:
    value = None
    next_element = None

    def __init__(self, value, next_element):
        self.value = value
        self.next_element = next_element


class Stack:
    top = None

    def push(self, value):
        self.top = Element(value, self.top)

    def pop(self):
        if self.top is None:
            return None
        value = self.top.value
        self.top = self.top.next_element
        return value


class Queue:
    front = None
    back = None

    def enqueue(self, value):
        new_element = Element(value, None)
        if self.back is not None:
            self.back.next_element = new_element
        self.back = new_element
        if self.front is None:
            self.front = new_element

    def dequeue(self):
        if self.front is None:
            return None
        value = self.front.value
        self.front = self.front.next_element
        return value


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
