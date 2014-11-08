def quicksort(num_array):
    """sorts num_array in-place
    returns None"""
    quicksort_subarray(num_array, 0, len(num_array))


def quicksort_subarray(num_array, left, right):
    """sorts in-place subarray of num_array from index left (inclusive) to right (exclusive)"""
    if left < right:
        sec_part_idx = partition(num_array, left, right)
        quicksort_subarray(num_array, left, sec_part_idx - 1)
        quicksort_subarray(num_array, sec_part_idx, right)


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


if __name__ == '__main__':
    import copy

    numbers = [3, 5, 4, 1, 8, 6, 2]
    numbers_sorted = [1, 2, 3, 4, 5, 6, 8]

    numbers_to_sort = copy.copy(numbers)
    quicksort(numbers_to_sort)
    assert numbers_to_sort == numbers_sorted
    print('All tests passed')
