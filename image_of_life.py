#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from life import read_life, ALIVE, DEAD

import ppm


if __name__ == '__main__':
    init = read_life()

    h, w = init.size()

    m = ppm.PixelMatrix(w, h)

    for x in range(m.get_width()):
        for y in range(m.get_height()):
            m.set_at((x, y), ppm.BinaryColor(init.get_at((h - y - 1, w - x - 1))))

    i = ppm.PBMImage(m)
    i.save_to(sys.argv[1] + '.pbm')
