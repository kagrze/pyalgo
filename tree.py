class Node:
    def __init__(self, key, value, parent):
        self.__key = key
        self.__value = value
        self.__parent = parent
        self.__left = None
        self.__right = None

    @property
    def value(self):
        return self.__value

    def get_node(self, key):
        if self.__key == key:
            return self
        if key < self.__key:
            return None if not self.__left else self.__left.get_node(key)
        else:
            return None if not self.__right else self.__right.get_node(key)

    def set_value(self, key, value):
        if self.__key == key:
            self.__value = value
        if key < self.__key:
            if not self.__left:
                self.__left = Node(key, value, self)
            else:
                self.__left.set_value(key, value)
        else:
            if not self.__right:
                self.__right = Node(key, value, self)
            else:
                self.__right.set_value(key, value)

    def get_node_for_min_key(self):
        return self if not self.__left else self.__left.get_node_for_min_key()

    def get_node_for_max_key(self):
        return self if not self.__right else self.__right.get_node_for_max_key()

    def as_ordered_list(self):
        to_return = [] if not self.__left else self.__left.as_ordered_list()
        to_return.append((self.__key, self.__value))
        if self.__right:
            to_return.extend(self.__right.as_ordered_list())
        return to_return

    def delete(self):
        """returns node that replaces removed node in the tree"""
        if not self.__left:
            if not self.__right:  # childless node
                if self.__parent:
                    if self.__parent.__left == self:
                        self.__parent.__left = None
                    else:
                        self.__parent.__right = None
                return None  # no one replaces deleted node
            else:  # only right child exists
                if self.__parent:
                    self.__right.__parent = self.__parent
                    if self.__parent.__left == self:
                        self.__parent.__left = self.__right
                    else:
                        self.__parent.__right = self.__right
                return self.__right  # node's right child replace node in the tree
        else:
            if not self.__right:  # only left child exists
                if self.__parent:
                    self.__left.__parent = self.__parent
                    if self.__parent.__left == self:
                        self.__parent.__left = self.__left
                    else:
                        self.__parent.__right = self.__left
                return self.__left  # node's left child replace node in the tree
            else:  # both children are present
                predecessor = self.__left.get_node_for_max_key()
                # swap self with predecessor
                predecessor.__key, self.__key = self.__key, predecessor.__key
                predecessor.__value, self.__value = self.__value, predecessor.__value
                # predecessor do not have right child so recursion will stop in the next invocation
                return predecessor.delete()


class Tree:
    """Binary Search Tree"""
    __root = None

    def set_value(self, key, value):
        if self.__root:
            self.__root.set_value(key, value)
        else:
            self.__root = Node(key, value, None)

    def get_value(self, key):
        if not self.__root:
            return None
        else:
            node = self.__root.get_node(key)
            return None if not node else node.value

    def as_ordered_list(self):
        return [] if not self.__root else self.__root.as_ordered_list()

    def get_value_for_min_key(self):
        return None if not self.__root else self.__root.get_node_for_min_key().value

    def get_value_for_max_key(self):
        return None if not self.__root else self.__root.get_node_for_max_key().value

    def delete_node(self, key):
        if not self.__root:
            return None
        node = self.__root.get_node(key)
        if not node:
            return None
        if self.__root == node:
            self.__root = node.delete()
        else:
            node.delete()


if __name__ == '__main__':
    t = Tree()
    t.set_value('k0', 1)
    assert t.as_ordered_list() == [('k0', 1)]
    t.set_value('k4', 2)
    assert t.as_ordered_list() == [('k0', 1), ('k4', 2)]
    t.set_value('k5', 3)
    assert t.as_ordered_list() == [('k0', 1), ('k4', 2), ('k5', 3)]
    t.set_value('k2', 4)
    assert t.as_ordered_list() == [('k0', 1), ('k2', 4), ('k4', 2), ('k5', 3)]
    t.set_value('k1', 5)
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k2', 4), ('k4', 2), ('k5', 3)]
    t.set_value('k3', 6)
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k2', 4), ('k3', 6), ('k4', 2), ('k5', 3)]

    assert t.get_value('k0') == 1
    assert t.get_value('k1') == 5
    assert t.get_value('k2') == 4
    assert t.get_value('k3') == 6
    assert t.get_value('k4') == 2
    assert t.get_value('k5') == 3
    assert t.get_value('k6') is None

    assert t.get_value_for_min_key() == 1
    assert t.get_value_for_max_key() == 3

    t.delete_node('k4')
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k2', 4), ('k3', 6), ('k5', 3)]
    t.delete_node('k4')
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k2', 4), ('k3', 6), ('k5', 3)]
    t.delete_node('k3')
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k2', 4), ('k5', 3)]
    t.delete_node('k2')
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k5', 3)]
    t.delete_node('k2')
    assert t.as_ordered_list() == [('k0', 1), ('k1', 5), ('k5', 3)]
    t.delete_node('k1')
    assert t.as_ordered_list() == [('k0', 1), ('k5', 3)]
    t.delete_node('k0')
    assert t.as_ordered_list() == [('k5', 3)]
    t.delete_node('k5')
    assert t.as_ordered_list() == []

    print('All tests passed')
