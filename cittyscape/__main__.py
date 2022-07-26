import sys
import curses

from cittyscape import StreetViewer, iter_buildings, iter_people, getkey


def main(scr, viewer):
    curses.mousemask(-1)
    curses.curs_set(0)
    curses.use_env(True)
    curses.noecho()
    curses.cbreak()
    curses.raw()
    curses.meta(1)
    scr.timeout(30)

    while True:
        try:
            if viewer.dx < viewer.max_speed:
                viewer.dx += 1
            if viewer.dx > viewer.max_speed:
                viewer.dx -= 1

            viewer.xoffset += viewer.dx
            viewer.draw(scr)
            ch = getkey(scr)
        except Exception as e:
            raise # return str(e)

        if not ch: continue
        if ch == '^Q': return

        if ch == '^L':
            scr.refresh()
        else:
            if viewer.handle_key(ch):
                break


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
