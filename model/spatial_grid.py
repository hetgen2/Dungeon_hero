import math
from utils import clamp


class UniformGrid:
    def __init__(self, cell_size, width, height):
        self.cell_size = cell_size
        self.cols = math.ceil(width / cell_size)
        self.rows = math.ceil(height / cell_size)
        self.cells =[]
        for row_number in range(self.rows):
            row=[]
            for col_number in range(self.cols):
                cell=[]
                row.append(cell)
            self.cells.append(row)
        

    def clear(self):
        for row in self.cells:
            for cell in row:
                cell.clear()

    def _cell_index(self, x, y):
        col = clamp(int(x // self.cell_size), 0, self.cols - 1)
        row = clamp(int(y // self.cell_size), 0, self.rows - 1)
        return col, row

    def insert(self, obj, x, y):
        col, row = self._cell_index(x, y)
        self.cells[row][col].append(obj)

    def query(self, x, y, radius):
        col, row = self._cell_index(x, y)
        reach = math.ceil(radius / self.cell_size)
        result = []
        for r in range(max(0, row - reach), min(self.rows, row + reach + 1)):
            for c in range(max(0, col - reach), min(self.cols, col + reach + 1)):
                result.extend(self.cells[r][c])
        return result
