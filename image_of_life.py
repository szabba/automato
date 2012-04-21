#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from life import read_life, DEAD, ALIVE

import ppm

if __name__ == '__main__':
    num = 0

    colors = {
            DEAD: ppm.RGBColor(1, (1, 1, 1)),
            ALIVE: ppm.RGBColor(1, (0, 0, 1))
    }

    while True:
        try:
            if num > 0:
                line = sys.stdin.readline()
                if not life in ['\n', '']:
                    print 'Life grid specs should be interspersed with newlines\
 and their list should end with an EOF.'
                    sys.exit(1)

            init = read_life()

            h, w = init.size()

            m = ppm.PixelMatrix(w, h)

            for x in range(m.get_width()):
                for y in range(m.get_height()):
                    m.set_at((x, y), colors[init.get_at((h - y - 1, w - x -
                        1))])

            i = ppm.PPMImage(m)
            i.save_to('%s_%d.ppm' % (sys.argv[1], num))
            num += 1

        except ValueError:
            break
