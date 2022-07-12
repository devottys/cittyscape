import sys
import curses

from asciitty import StreetViewer, iter_buildings, main

if __name__ == '__main__':
    argc = len(sys.argv)
    startblock = 0
    endblock = 1000
    if argc > 1:
        startblock = int(sys.argv[1], base=16)
        endblock = startblock + 256
    if argc > 2:
        endblock = int(sys.argv[2], base=16)

    viewer = StreetViewer()
    viewer.load(iter_buildings(startblock, endblock))
    curses.wrapper(main, viewer)
