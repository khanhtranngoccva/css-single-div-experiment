import numpy
from tqdm import tqdm

FloatingColorPoint = tuple[int | float, int | float, int | float]


def is_adjacent_color(color: FloatingColorPoint, cmp: FloatingColorPoint, tolerance: int):
    r, g, b = color
    c_r, c_g, c_b = cmp

    return abs(r - c_r) <= tolerance and abs(g - c_g) <= tolerance and abs(b - c_b) <= tolerance


def add_tuple(t1: FloatingColorPoint, t2: FloatingColorPoint):
    r1, g1, b1 = t1
    r2, g2, b2 = t2

    return r1 + r2, g1 + g2, b1 + b2


def mul_tuple(t1: FloatingColorPoint, multiplier: int | float) -> FloatingColorPoint:
    r1, g1, b1 = t1
    return r1 * multiplier, g1 * multiplier, b1 * multiplier


def divide_tuple(t1: FloatingColorPoint, divisor: int | float) -> FloatingColorPoint:
    r1, g1, b1 = t1

    return r1 / divisor, g1 / divisor, b1 / divisor


# This part is rewritten from scratch, but the idea is from Junferno.
def bfs_image_matrix(matrix: list[list[tuple[int, int, int]]], *, tolerance=10, min_points=50, progress=True):
    width = len(matrix[0])
    height = len(matrix)

    # Visited regions
    visited = numpy.zeros((height, width), bool)

    def get_point(x: int, y: int):
        return matrix[y][x]

    def get_adjacent_coords(x: int, y: int):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_coords = []

        for dir_x, dir_y in directions:
            new_x = x + dir_x
            new_y = y + dir_y

            if 0 <= new_x < width and 0 <= new_y < height:
                adjacent_coords.append((new_x, new_y))

        return adjacent_coords

    def start_breadth_search(x: int, y: int):
        # First, initialize by creating a queue with an initial point, a points counter, an
        # average color, and a final contiguous region map.
        contiguous_region = numpy.zeros((height, width), numpy.int8)

        contiguous_region.fill(255)
        queue = [(x, y)]
        points = 0
        initial = get_point(x, y)
        avg = (0, 0, 0)

        # Search stops once queue is emptied out.
        while len(queue) > 0:
            cur_x, cur_y = queue.pop()
            cur_color = get_point(cur_x, cur_y)

            # Early return if point is not matching or has already been visited
            if visited[cur_y][cur_x]: continue
            if not points == 0 and not is_adjacent_color(cur_color, initial, tolerance): continue

            contiguous_region[cur_y][cur_x] = 0
            visited[cur_y][cur_x] = True

            # Set new average
            prev_sum = mul_tuple(avg, points)
            points += 1
            new_sum = add_tuple(prev_sum, cur_color)
            avg = divide_tuple(new_sum, points)

            # Get adjacent coordinates and push into the queue:
            for coord in get_adjacent_coords(cur_x, cur_y):
                queue.append(coord)

        if points >= min_points:
            return contiguous_region, initial

    iterator = tqdm(range(width)) if progress else range(width)
    for i in iterator:
        for j in range(height):
            if not visited[j][i]:
                region = start_breadth_search(i, j)
                if region is not None:
                    yield region
