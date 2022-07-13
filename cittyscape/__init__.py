#!/usr/bin/env python3

from collections import defaultdict
import sys
import curses

from wcwidth import wcswidth

from .buildings import iter_buildings
from .utils import Colors

keycodes = { getattr(curses, k):k for k in dir(curses) if k.startswith('KEY_') }
keycodes.update({chr(i): '^'+chr(64+i) for i in range(32)})

MINDX=0.015
INCRDX = 0.1

def getkey(scr):
    try:
        ch = scr.get_wch()
        return keycodes.get(ch, ch)
    except curses.error:
        return ''


def main(scr, viewer):
    global colors

    curses.mousemask(-1)
    curses.curs_set(0)
    curses.use_env(True)
    curses.noecho()
    curses.cbreak()
    curses.raw()
    curses.meta(1)
    scr.timeout(30)

    colors = Colors()

    while True:
        try:
            if viewer.dx < viewer.max_speed:
                viewer.dx += MINDX
            if viewer.dx > viewer.max_speed:
                viewer.dx -= MINDX

            viewer.xoffset += viewer.dx
            viewer.draw(scr)
            ch = getkey(scr)
        except Exception as e:
            return str(e)

        if not ch: continue
        if ch == '^Q': return

        if ch == '^L':
            scr.refresh()
        else:
            if viewer.handle_key(ch):
                break


class StreetViewer:
    def __init__(self):
        self.layout = defaultdict(lambda: defaultdict(list))
        self._status = ''
        self.xoffset = self.dx = 0
        self.yoffset = 0
        self.max_speed = 0

    def load(self, buildings):
        for bldg in sorted(buildings, key=lambda r: r.box.y2):
            for r in bldg:
                if not r.text: continue
                r.textwidth = wcswidth(r.text)
                if not r.textwidth: continue
                self.layout[r.x][r.y].append(r)

    def status(self, s):
        self._status = str(s)

    def draw(self, scr):
        scr.erase()
        scr.bkgd(' ', colors.get('on 232'))

        h, w = scr.getmaxyx()
        self.yoffset = 50-h + 15
        scr.addstr(h-1, 0, f'{self.xoffset:0.0f} +{self.dx:0.1f} {self._status}')

        for y in range(0, h):
            x = 0
            while x < w-1:
                rows = self.layout[x+int(self.xoffset)][y+self.yoffset]
                if not rows:
                    x += 1
                    continue
                row = rows[-1]
                rw = row.textwidth
                if not rw:
                    x += 1
                    continue

                scr.addstr(y, x, row.text, colors.get(row.color))
                x += rw

    def handle_key(self, ch):
        'Return True to exit.'
        if ch == 'q': return True
        elif ch in ['l', 'KEY_RIGHT']: self.max_speed = min(self.max_speed+INCRDX, 4)
        elif ch in ['h', 'KEY_LEFT']: self.max_speed = max(self.max_speed-INCRDX, 0)
        elif ch in ['k', 'KEY_UP']: self.yoffset -= 3
        elif ch in ['j', 'KEY_DOWN']: self.yoffset += 3
        elif ch in ['KEY_NPAGE']: self.xoffset += 128
        elif ch in ['KEY_PPAGE']: self.xoffset -= 128
        else:
            self.status(f'unknown key {ch}')
