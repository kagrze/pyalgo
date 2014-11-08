def insert(element, sorted_array):
    if len(sorted_array) == 0:
        to_return = [element]
    elif element < sorted_array[0]:
        to_return = [element]
        to_return.extend(sorted_array)
    else:
        to_return = [sorted_array[0]]
        to_return.extend(insert(element, sorted_array[1:]))
    return to_return


def insertionsort(num_array):
    return num_array if len(num_array) == 0 else insert(num_array[0], insertionsort(num_array[1:]))


if __name__ == '__main__':
    numbers = [3, 5, 4, 1, 8, 6, 1]
    numbers_sorted = [1, 1, 3, 4, 5, 6, 8]
    assert insertionsort(numbers) == numbers_sorted
    print('All tests passed')
