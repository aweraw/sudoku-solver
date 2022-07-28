from collections import defaultdict
from functools import reduce

vgroups = [[(x, y) for y in range(9)] for x in range(9)]
hgroups = [[(x, y) for x in range(9)] for y in range(9)]
lgroups = [
    [(x, y) for y in range(a, a+3) for x in range(b, b+3)]
    for a in range(0, 9, 3) for b in range(0, 9, 3)]

ec_keys = reduce(lambda x, y: x+y, hgroups) + \
          [(c, g, v) for c in 'hvl' for g in range(9) for v in range(1, 10)]


def local_group(x, y):
    if x < 3:
        xs = set([0, 3, 6])
    elif x < 6:
        xs = set([1, 4, 7])
    else:
        xs = set([2, 5, 8])

    if y < 3:
        ys = set([0, 1, 2])
    elif y < 6:
        ys = set([3, 4, 5])
    else:
        ys = set([6, 7, 8])

    return xs.intersection(ys).pop()


def groups(x, y):
    return hgroups[y], vgroups[x], lgroups[local_group(x, y)]


def exact_cover(keys, rows, need=81):
    # if we have no keys, we've found a solution
    if not keys:
        return []
    # get number of set values in each column
    col_sums = [sum(row[k] for row in rows) for k in keys]
    # if any columns have no rows set, then there is no solution
    if not all(col_sums):
        return []
    # get the column (key) with the least set rows
    k = keys[col_sums.index(min(col_sums))]
    # select the rows with the column (k) set above
    rs = [r for r in rows if r[k]]
    # remove the selected rows from the collection
    rows = [r for r in rows if r not in rs]
    # iterate through candidate rows and find the longest
    # and therefore correct solution
    solutions = list()
    for row in rs:
        # find the keys set on row
        ks = [k for k in row if row[k]]
        # remove the set keys from the collection
        fkeys = [k for k in keys if k not in ks]
        # remove any rows which have any of the same keys set
        frows = [
            r for r in rows
            if not any((r[ks[0]], r[ks[1]], r[ks[2]], r[ks[3]]))]
        solution = [(ks[0], ks[1][2])] + exact_cover(fkeys, frows, need-1)
        # if the solution contains the number of elements we need, return it
        if len(solution) == need:
            return solution
    # we didn't find a solution containing the number of elements we needed
    # terminate branch
    return []


class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.ngrid = [
            [set(range(1, 10)) for x in range(9)] for y in range(9)]
        self.ec_matrix = list()
        self.init_ngrid()
        self.init_ec_matrix()

    def eliminate(self, n, groups):
        for x, y in set(reduce(lambda x, y: x+y, groups)):
            if n in self.ngrid[y][x]:
                self.ngrid[y][x].remove(n)

    def init_ngrid(self):
        for group in hgroups:
            for x, y in group:
                if self.grid[y][x]:
                    v = self.grid[y][x]
                    self.eliminate(v, groups(x, y))
                    self.ngrid[y][x] = set([v])

    def init_ec_matrix(self):
        for y, row in enumerate(self.ngrid):
            for x, s in enumerate(row):
                for e in s:
                    d = defaultdict(int)
                    d[(x, y)] = 1
                    d[('h', y, e)] = 1
                    d[('v', x, e)] = 1
                    d[('l', local_group(x, y), e)] = 1
                    self.ec_matrix.append(d)

    def solve(self):
        solution = exact_cover(ec_keys, self.ec_matrix)
        for xy, v in solution:
            x, y = xy
            self.grid[y][x] = v

    def __repr__(self):
        s = list()
        for row in self.grid:
            s.append('  '.join(map(str, zip(*[iter(row)]*3))))
        return '\n\n'.join('\n'.join(x) for x in zip(*[iter(s)]*3))

    def __str__(self):
        return self.__repr__()


def solve(sudoku):
    grid = list(map(lambda x: list(map(int, x)), zip(*[iter(sudoku)]*9)))
    s = Sudoku(grid)
    s.solve()
    return ''.join(''.join(str(n) for n in x) for x in s.grid)
