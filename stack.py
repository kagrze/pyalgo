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


if __name__ == '__main__':
    s = Stack()
    s.push(5)
    s.push(3)
    s.push(-1)

    assert s.pop() == -1
    assert s.pop() == 3
    assert s.pop() == 5
    assert s.pop() is None

    print('All tests passed')
