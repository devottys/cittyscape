import sys
import curses

from cittyscape import StreetViewer, iter_buildings, iter_people, main

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
    viewer.load(iter_people())
    curses.wrapper(main, viewer)
