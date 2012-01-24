#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random, sys, optparse, time, re

class Grid(list):
    def __init__(self, size=10, chance=(1, 10), birth=[3], survival=[2, 3],
            empty=False):
        super(list, self).__init__()

        self.size = size
        self.birth = birth
        self.survival = survival
        count, maxi = chance

        for _ in range(size):
            self.append([])

            for _ in range(size):
                if empty:
                    self[-1].append(0)
                else:
                    self[-1].append(1 if random.randint(1, maxi) in range(1,
                        count + 1) else 0)

    def next_cell(self, i, j):
        count = 0

        for di in range(-1, 2):
            for dj in range(-1, 2):
                # Wrap arround last column and row. Wrapping around the first
                # ones is automatic as -1 is a valid index in Python.
                if i == self.size - 1 and di == 1:
                    di = -self.size - 1
                if j == self.size - 1 and dj == 1:
                    dj = -self.size - 1

                if self[i + di][j + dj] and (di, dj) != (0, 0):
                    count += 1
        
        alive = self[i][j]
        survival = self.survival
        birth = self.birth

        if (alive and count in survival) or ((not alive) and count in birth):
            return 1
        else:
            return 0

    def next_grid(self):
        next = Grid(self.size, empty=True)
        count = 0

        for i in range(self.size):
            for j in range(self.size):
                next[i][j] = self.next_cell(i, j)
                count += next[i][j]

        return next, count

    def print_grid(self, repeat_x=1, repeat_y=1):
        output = ''
        for _ in range(repeat_y):
            for line in self:
                for _ in range(repeat_x):
                    for point in line:
                        if point:
                            output += '#'
                        else:
                            output += ' '
                output += '\n'
        print output

def interactive(grid, count):
    try:
        line = raw_input()
    except EOFError:
        return True
    
    return line == 'q'

def n_steps(n):
    step_dict = {'n': n}
    def inner(grid, count):
        if step_dict['n'] == 0:
            return True
        else:
            step_dict['n'] -= 1
            return False
    return inner

def die_of_boredom(cond):
    def inner(grid, count):
        if count == 0:
            return True
        else:
            return cond(grid, cond)

    return inner

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [options]')

    parser.add_option('-b', '--birth',
            help='Birth rules.',
            dest='birth', metavar='BIRTH',
            action='store', default='3')
    parser.add_option('-s', '--survival',
            help='Survival rules.',
            dest='survival', metavar='SURVIVAL',
            action='store', default='23')
    parser.add_option('-i', '--interactive',
            help='''Interactive mode. Type "q" to quit, type nothing to
            continue. This makes life ignore the -I and -z options.''',
            dest='interactive', action='store_true', default=False)
    parser.add_option('-z', '--Zzz',
            help='Sleep time in miliseconds.',
            dest='sleep', metavar='SLEEP',
            action='store', type='int', default=1000)
    parser.add_option('-I', '--iteration-steps',
            help='How many times to iterate the game of life.',
            dest='step_count', metavar='STEPS',
            action='store', type='int', default=1000)
    parser.add_option('-S', '--size',
            help='Size of the grid.',
            dest='size', metavar='SIZE',
            action='store', type='int', default=10)
    parser.add_option('-c', '--chance',
            help='The chance a cell has of being initially alive.',
            dest='chance', metavar='CHANCE',
            action='store', default='1:10')
    parser.add_option('-x', '--repeat-x',
            help='''Number of horizontal repetitions of the grid in the
            output.''',
            dest='repeat_x', metavar='REPEAT_X',
            action='store', type='int', default=1)
    parser.add_option('-y', '--repeat-y',
            help='''Number of vertical repetitions of the grid in the
            output.''',
            dest='repeat_y', metavar='REPEAT_Y',
            action='store', type='int', default=1)
    parser.add_option('-D', '--die-of-boredom',
            help='''End the program when everythin dies. This doesn't supress
            normal ending conditions.''',
            dest='die_of_boredom', action='store_true', default=False)

    opts, args = parser.parse_args(sys.argv[1:])

    # The --chance option requires some more sophisticated handling.
    if not re.match(r'\d+:\d+', opts.chance):
        parser.error('''The --chance option's value must be of form n:m, where n
                and m are natural numbers.''')
    else:
        chance = tuple([int(p) for p in opts.chance.split(':')])

    grid = Grid(opts.size, chance,
            [int(c) for c in opts.birth],
            [int(c) for c in opts.survival])

    finished = False
    if opts.interactive:
        cond = interactive
    else:
        cond = n_steps(opts.step_count)

    if opts.die_of_boredom:
        cond = die_of_boredom(cond)

    while not finished:
        grid.print_grid(opts.repeat_x, opts.repeat_y)
        grid, count = grid.next_grid()

        finished = cond(grid, count)
