# Use this for debugging, if needed
def pretty_print(matrix):
    print('-' * (len(matrix[0]) * 2 - 1))
    for row in matrix:
        print(' '.join(str(item) for item in row))
    print('-' * (len(matrix[0]) * 2 - 1))


def get_column(matrix, column):
    if column >= 0 and column < len(matrix[0]):
        return [row[column] for row in matrix]
    else:
        print(f"{column} is not a valid column index for the matrix.")
        return []

def rotate_clockwise(matrix):
    return [get_column(matrix, column)[::-1] for column in range(len(matrix[0]))]

def rotate_counterclockwise(matrix):
    return [get_column(matrix, column) for column in range(len(matrix[0]))[::-1]]

def flip_horizontal(matrix):
    return [row[::-1] for row in matrix]

def flip_vertical(matrix):
    return matrix[::-1]

matrix_1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

expected_clockwise_1 = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
expected_counterclockwise_1 = [[3, 6, 9], [2, 5, 8], [1, 4, 7]]
expected_flip_horizontal_1 = [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
expected_flip_vertical_1 = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]

assert rotate_clockwise(matrix_1) == expected_clockwise_1
assert rotate_counterclockwise(matrix_1) == expected_counterclockwise_1
assert flip_horizontal(matrix_1) == expected_flip_horizontal_1
assert flip_vertical(matrix_1) == expected_flip_vertical_1


matrix_2 = [[1, 2], [3, 4], [5, 6], [7, 8]]

expected_clockwise_2 = [[7, 5, 3, 1], [8, 6, 4, 2]]
expected_counterclockwise_2 = [[2, 4, 6, 8], [1, 3, 5, 7]]
expected_flip_horizontal_2 = [[2, 1], [4, 3], [6, 5], [8, 7]]
expected_flip_vertical_2 = [[7, 8], [5, 6], [3, 4], [1, 2]]

assert rotate_clockwise(matrix_2) == expected_clockwise_2
assert rotate_counterclockwise(matrix_2) == expected_counterclockwise_2
assert flip_horizontal(matrix_2) == expected_flip_horizontal_2
assert flip_vertical(matrix_2) == expected_flip_vertical_2


matrix_3 = [[1, 2, 3], [4, 5, 6]]

expected_clockwise_3 = [[4, 1], [5, 2], [6, 3]]
expected_counterclockwise_3 = [[3, 6], [2, 5], [1, 4]]
expected_flip_horizontal_3 = [[3, 2, 1], [6, 5, 4]]
expected_flip_vertical_3 = [[4, 5, 6], [1, 2, 3]]

assert rotate_clockwise(matrix_3) == expected_clockwise_3
assert rotate_counterclockwise(matrix_3) == expected_counterclockwise_3
assert flip_horizontal(matrix_3) == expected_flip_horizontal_3
assert flip_vertical(matrix_3) == expected_flip_vertical_3