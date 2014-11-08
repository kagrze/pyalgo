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


def mergesort(num_array):
    if len(num_array) == 1:
        return num_array
    if len(num_array) == 2:
        return num_array if num_array[0] < num_array[1] else [num_array[1], num_array[0]]
    half_size = int(len(num_array) / 2)
    return merge(
        mergesort(num_array[0:half_size]),
        mergesort(num_array[half_size:])
    )


if __name__ == '__main__':
    numbers = [3, 5, 4, 1, 8, 6, 1]
    numbers_sorted = [1, 1, 3, 4, 5, 6, 8]
    assert mergesort(numbers) == numbers_sorted
    print('All tests passed')
