from typing import List, Tuple, Union

import numpy as np

from models.tables import ImageTable, Table, Cell, ImageCell, TesseractTable


def find_borders(cells: List[Union[ImageCell, Cell]]) -> Tuple[int, int, int, int]:
    left_x = 1e10
    right_x = 0
    top_y = 1e10
    bottom_y = 0
    for cell in cells:
        if cell.coordinates[0] < top_y:
            top_y = cell.coordinates[0]
        if cell.coordinates[0] > bottom_y:
            bottom_y = cell.coordinates[0]
        if cell.coordinates[1] < left_x:
            left_x = cell.coordinates[1]
        if cell.coordinates[1] > right_x:
            right_x = cell.coordinates[1]
    return left_x, top_y, right_x, bottom_y


def find_min_size(cells: List[Union[ImageCell, Cell]]) -> Tuple[int, int]:
    min_size = (1e10, 1e10)
    for cell in cells:
        if cell.size[0] <= min_size[0] or cell.size[1] <= min_size[1]:
            min_size = cell.size
    return min_size


def quantize_cells(
        cells: List[Cell], grid: List[Tuple[int, int]], min_size: Tuple[int, int], borders
) -> List[Cell]:
    quantized_cells = []
    for cell in cells:

        # Quantize cell's coordinates

        coordinates = list(cell.coordinates[::-1])
        coordinates[0] = (coordinates[0] - borders[0]) // min_size[0]
        coordinates[1] = (coordinates[1] - borders[1]) // min_size[1]

        # print(closest_grid_point)
        new_cell = cell
        # print(closest_grid_point_0, closest_grid_point_1)
        # print("---")
        new_cell.coordinates = tuple(coordinates)

        # Quantize cell size

        size = cell.size
        size_0 = int(np.round(size[0] / min_size[0]))
        size_1 = int(np.round(size[1] / min_size[1]))

        new_cell.size = (size_1, size_0)

        quantized_cells.append(new_cell)

    return quantized_cells


def generate_table_from_image(image_table: ImageTable) -> Table:
    table: Table = Table()
    min_size = find_min_size(image_table.cells)
    image_size = image_table.image.shape[:2]
    grid = [
        (i, k)
        for i in range(0, image_size[1] + min_size[0], min_size[0])
        for k in range(0, image_size[0] + min_size[1], min_size[1])
    ]

    # TODO

    return table


def generate_table_from_tesseract(tesseract_table: TesseractTable) -> Table:
    table: Table = Table()
    tesseract_table.cells = [
        cell
        for cell in tesseract_table.cells
        if cell.size[0] > 12 and cell.size[1] > 12 and cell.content is not None
    ]
    min_size = find_min_size(tesseract_table.cells)
    borders = find_borders(tesseract_table.cells)
    # print(min_size)
    # print(borders)
    grid = [
        (i, k)
        for i in range(borders[0], borders[2] + min_size[0], min_size[0])
        for k in range(borders[1], borders[3] + min_size[1], min_size[1])
    ]

    quantized_cells = quantize_cells(tesseract_table.cells, grid, min_size, borders)
    table.cells = quantized_cells
    table.dimensions = (
        (borders[3] - borders[1]) // min_size[1] + 1,
        (borders[2] - borders[0]) // min_size[0] + 1,
    )
    table.fill_table()
    table.sort_table()
    # print([cell.coordinates for cell in table.cells])
    table.gen_rows()

    return table
