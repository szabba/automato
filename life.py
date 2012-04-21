#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random, sys, optparse, time, re

from automato import Automata, RectGrid, moore

# Contstants

H, W = 20, 20

LIFE_PROBABLITY = 0.4

ALIVE, DEAD = 1, 0

def life_rule(birth=[3], survival=[2, 3]):

    def rule(cell, neighbours):

        if cell is ALIVE and sum(neighbours) in survival:
            return ALIVE

        elif sum(neighbours) in birth:
            return ALIVE

        else:
            return DEAD

    return rule


def random_fill(grid, p):

    for pos in grid.indices():

        if random.random() <= p:
            grid.set_at(pos, ALIVE)
        else:
            grid.set_at(pos, DEAD)


def print_grid(grid):
    y_prev = 0

    for y, x in grid.indices():

        if y != y_prev:
            sys.stdout.write('\n')
            y_prev = y

        if grid.get_at((y, x)) == ALIVE:
            sys.stdout.write('@')
        else:
            sys.stdout.write('_')

    sys.stdout.write('\n' * 2)


def read_life():
        spec_line = sys.stdin.readline()[:-1]

        if not re.match(r'\d+ \d+', spec_line):
            raise ValueError('''A stdin input must start with a line specifying the
                    height and widht split by a space.''')

        spec_parts = spec_line.split(' ')
        h, w = map(int, spec_parts)

        init = RectGrid(h, w)

        cells = []
        for y in range(h):
            line = sys.stdin.readline()[:-1]

            if len(line) != w:
                raise  ValueError('''Line %d should be of length %d and not %d.''' %
                        (y + 1, w, len(line)))

            for c in line:
                if c == '@':
                    cells.append(ALIVE)
                else:
                    cells.append(DEAD)

        for pos, c in zip(init.indices(), cells):
            init.set_at(pos, c)

        return init


if __name__ == '__main__':

    # Parse the options

    parser = optparse.OptionParser(usage='usage: %prog [options]')

    parser.add_option('-z', '--Zzz',
            help='Sleep time in miliseconds.',
            dest='sleep', metavar='SLEEP',
            action='store', type='int', default=0)

    parser.add_option('-r', '--rule',
            help='Rule variant',
            dest='rule', metavar='RULE',
            action='store', type='str', default='3/23')

    parser.add_option('-I', '--iterations',
            help='sleep time in miliseconds.',
            dest='iter', metavar='ITER',
            action='store', type='int', default=1000)

    parser.add_option('-i', '--stdin',
            help='Read initial state from stdin.',
            dest='stdin', metavar='STDIN',
            action='store_true', default=False)

    parser.add_option('-w', '--wrap',
            help='Put Life under periodic edge conditions.',
            dest='periodic', metavar='PERIODIC',
            action='store_true', default=False)

    parser.add_option('-s', '--print-size',
            help='Print the spec line before each grid printout.',
            dest='print_size', metavar='PRINT_SIZE',
            action='store_true', default=False)

    opts, args = parser.parse_args(sys.argv[1:])

    # Parse rule
    if not re.match(r'\d?/\d?', opts.rule):
        parser.error('''The --rule option must be followed by a proper life
                rule.''')

    else:
        birth, survival = opts.rule.split('/')

        birth = [int(c) for c in birth]
        survival = [int(c) for c in survival]

    # Initialise grid
    if not opts.stdin:
        init = RectGrid(H, W)
        random_fill(init, LIFE_PROBABLITY)

    else:
        try:
            init = read_life()
        except ValueError as e:
            print 'An error occured while parsing the input.\n\n'
            print e
            sys.exit(1)

    # Run the automata
    life = Automata(init, moore(0, periodic=opts.periodic),
            life_rule(birth, survival))

    h, w = init.size()
    if opts.print_size:
        print '%d %d' % (h, w)
    print_grid(init)
    del init

    for _ in range(opts.iter - 1):

        current = life.perform_step()
        if opts.print_size:
            print '%d %d' % (h, w)
        print_grid(current)
