def insertionsort(num_array):
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

    return num_array if len(num_array) == 0 else insert(num_array[0], insertionsort(num_array[1:]))


def mergesort(num_array):
    def merge(lhs, rhs):
        merged = []
        i = 0
        j = 0
        for k in range(len(lhs) + len(rhs)):
            if i == len(lhs) or j < len(rhs) and lhs[i] > rhs[j]:
                merged.append(rhs[j])
                j += 1
            else:
                merged.append(lhs[i])
                i += 1
        return merged

    if len(num_array) == 1:
        return num_array
    if len(num_array) == 2:
        return num_array if num_array[0] < num_array[1] else [num_array[1], num_array[0]]
    half_size = int(len(num_array) / 2)
    return merge(
        mergesort(num_array[0:half_size]),
        mergesort(num_array[half_size:])
    )


def quicksort(num_array):
    """sorts num_array in-place
    returns None"""
    def quicksort_subarray(left, right):
        """sorts in-place subarray of num_array from index left (inclusive) to right (exclusive)"""
        if left < right:
            sec_part_idx = partition(num_array, left, right)
            quicksort_subarray(left, sec_part_idx - 1)
            quicksort_subarray(sec_part_idx, right)

    def partition(num_array, left, right):
        """partition in-place subarray of num_array from index left (inclusive) to right (exclusive)
        returns an index of a beginning of the second partition
        implementation assumes that pivot is the first element of an array"""
        pivot = num_array[left]
        i = left + 1
        for j in range(left + 1, right):
            if num_array[j] < pivot:
                num_array[i], num_array[j] = num_array[j], num_array[i]
                i += 1
        num_array[left], num_array[i - 1] = num_array[i - 1], num_array[left]  # placing a pivot in a proper place
        return i

    quicksort_subarray(0, len(num_array))


if __name__ == '__main__':
    from copy import copy

    numbers = [3, 5, 4, 1, 8, 6, 1]
    numbers_sorted = [1, 1, 3, 4, 5, 6, 8]

    assert insertionsort(numbers) == numbers_sorted
    assert mergesort(numbers) == numbers_sorted

    numbers_to_sort = copy(numbers)
    quicksort(numbers_to_sort)
    assert numbers_to_sort == numbers_sorted

    print('All tests passed')
