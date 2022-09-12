
from collections import defaultdict
from copy import copy

from wcwidth import wcswidth

from cittyscape import colors, sunset_color


class StreetViewer:
    def __init__(self, mindx=0.015, incrdx=0.15):
        self.layout = defaultdict(lambda: defaultdict(list))
        self._status = ''
        self.xoffset = self.dx = 0
        self.yoffset = 0
        self.max_speed = 0
        self.incrdx = incrdx
        self.time = 6*3600+850  # start at sunrise

    def load(self, things):
        for thing in things: # sorted(things, key=lambda r: r.box.y2):
            for actual_row in thing.itertext():
                if not actual_row.text: continue
                lines = actual_row.text.splitlines()

                for dy, line in enumerate(lines):
                    r = copy(actual_row)
                    r.text = line
                    r.textwidth = max(map(wcswidth, lines))
                    r.y -= dy - len(lines)

                    self.layout[r.x][r.y].append(r)

    def status(self, s):
        self._status = str(s)

    @property
    def timestr(self):
        h = int(self.time // 3600)
        m = int((self.time % 3600) // 60)
        return f'{h:02d}:{m:02d}'

    def step(self, dt=1):
        if self.max_speed >= 0 and self.dx < self.max_speed:
            self.dx += dt
        if self.max_speed >= 0 and self.dx > self.max_speed:
            self.dx -= dt
        if self.max_speed <= 0 and self.dx > self.max_speed:
            self.dx -= dt
        if self.max_speed <= 0 and self.dx < self.max_speed:
            self.dx += dt

        if abs(self.dx) > 0.1:
            self.xoffset += self.dx

        self.time += dt

    def draw(self, scr):
        scr.erase()
        scr.bkgd(' ', colors.get('on 232'))

        h, w = scr.getmaxyx()
        scr.addstr(h-1, 0, f'{self.timestr} dx={self.xoffset:0.0f} dy={self.yoffset:0.0f} +{self.dx:0.1f} {self._status} h={h}')

        for y in range(0, h-1):   # y=0 at bottom of window; y=-1 on status line
            if y > 16:
                fg, bg, ch = sunset_color(self.time*60+y*95)
                scr.addstr(h-2-y, 0, ch*(w-1), colors.get(f'{fg} on {bg}'))

            x = 0
            while x < w-1:
                rows = self.layout[x+int(self.xoffset)][y+int(self.yoffset)]
                if not rows:
                    x += 1
                    continue
                row = rows[-1]
                rw = row.textwidth
                if not rw:
                    x += 1
                    continue

                scr.addstr(h-2-y, x, row.text, colors.get(row.color))
                x += rw

    def handle_key(self, ch):
        'Return True to exit.'
        if ch == 'q': return True
        elif ch in ['0']: self.max_speed = 0
        elif ch in ['l', 'KEY_RIGHT']: self.max_speed = min(self.max_speed+self.incrdx, 4)
        elif ch in ['h', 'KEY_LEFT']: self.max_speed = max(self.max_speed-self.incrdx, -4)
        elif ch in ['k', 'KEY_UP']: self.yoffset += 1
        elif ch in ['j', 'KEY_DOWN']: self.yoffset -= 1
        elif ch in ['KEY_NPAGE']: self.xoffset += 128
        elif ch in ['KEY_PPAGE']: self.xoffset -= 128
        else:
            self.status(f'unknown key {ch}')
