#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import copy


class Automata(object):

    def __init__(self, grid, neighbourhood, rule):
        self.__current = grid
        self.__next = copy.deepcopy(grid)
        self.__neigbourhood = neighbourhood
        self.__rule = rule

    def perform_step(self):
        for pos in self.__current.indices():
            cell = self.__rule(self.__current.get_at(pos),
                    self.__neigbourhood(self.__current, pos))
            self.__next.set_at(pos, cell)

        self.__current, self.__next = self.__next, self.__current

        return self.__current


class RectGrid(object):

    def __init__(self, height, width):
        self.__h = height
        self.__w = width

        self.__grid = []

        for _ in range(self.__h):
            self.__grid.append([])

            for _ in range(self.__w):
                self.__grid[-1].append(None)

    def get_at(self, pos):
        y, x = pos
        return self.__grid[y][x]

    def set_at(self, pos, v):
        y, x = pos
        self.__grid[y][x] = v

    def indices(self):
        if not hasattr(self, '__indices'):
            self.__indices = []
            for y in range(self.__h):
                for x in range(self.__w):
                    self.__indices.append((y, x))

        return self.__indices

    def size(self):
        return (self.__h, self.__w)


def von_neumann(none=None, none_for_nonexistent=True, periodic=False):

    def neighbourhood(grid, pos):
        y, x = pos
        neighbours = []
        h, w = grid.size()

        for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:

            y_, x_ = y + dy, x + dx

            if periodic:
                # Don't check for -1, as Python handles it properly!

                if y_ == h:
                    y_ = 0

                if x_ == w:
                    x_ = 0

                pos_ = (y_, x_)
                cell = grid.get_at(pos_)

                neighbours.append(cell)

            elif none_for_nonexistent:

                if (y_ < 0) or (y_ >= h) or (x_ < 0) or (x_ >= w):
                    cell = none

                else:
                    pos_ = (y_, x_)
                    cell = grid.get_at(pos_)

                neighbours.append(cell)

            else:

                continue


        return neighbours

    return neighbourhood


def moore(none=None, none_for_nonexistent=True, periodic=False):

    def neighbourhood(grid, pos):
        y, x = pos
        neighbours = []
        h, w = grid.size()

        for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)]:

            y_, x_ = y + dy, x + dx

            if periodic:
                # Don't check for -1, as Python handles it properly!

                if y_ == h:
                    y_ = 0

                if x_ == w:
                    x_ = 0

                pos_ = (y_, x_)
                cell = grid.get_at(pos_)

                neighbours.append(cell)

            elif none_for_nonexistent:

                if (y_ < 0) or (y_ >= h) or (x_ < 0) or (x_ >= w):
                    cell = none

                else:
                    pos_ = (y_, x_)
                    cell = grid.get_at(pos_)

                neighbours.append(cell)

            else:

                continue


        return neighbours

    return neighbourhood


class HexGrid(object):

    def __init__(self, size):
        self.__size = size

        self.__grid = []

        for l in range(size, 2 * size) + range(2 * size - 2, size - 1, -1):
            self.__grid.append([None] * l)

    def get_at(self, pos):
        y, x = pos
        return self.__grid[y][x]

    def set_at(self, pos):
        y, x = pos
        self.__grid[y][x] = v

    def indices(self):
        if not hasattr(self, '__indices'):
            self.__indices = []

            for y, row in enumerate(self.__grid):
                for x, _ in enumerate(row):
                    self.__indices.append((y, x))

        return self.__indices


def hex_ring(grid, pos, none_for_nonexistent=True, none=None):
    y, x = pos
    neighbours = []

    for dy, dx in [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]:
        try:
            cell = grid.get_at(y + dy, x + dx)
        except IndexError:
            if none_for_nonexistent:
                cell = none
            else:
                continue

        neighbours.append(cell)

    return neighbours


if __name__ == '__main__':
    pass
