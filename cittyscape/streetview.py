
from collections import defaultdict

from wcwidth import wcswidth

from cittyscape import colors, sunset_color


class StreetViewer:
    def __init__(self, mindx=0.015, incrdx=0.1):
        self.layout = defaultdict(lambda: defaultdict(list))
        self._status = ''
        self.xoffset = self.dx = 0
        self.yoffset = 0
        self.max_speed = 0
        self.incrdx = incrdx
        self.time = 5*3600+850  # start at sunrise

    def load(self, buildings):
        for bldg in sorted(buildings, key=lambda r: r.box.y2):
            for r in bldg:
                if not r.text: continue
                r.textwidth = wcswidth(r.text)
                if not r.textwidth: continue
                self.layout[r.x][r.y].append(r)

    def status(self, s):
        self._status = str(s)

    @property
    def timestr(self):
        h = self.time // 3600
        m = (self.time % 3600) // 60
        return f'{h:02d}:{m:02d}'

    def draw(self, scr):
        scr.erase()
        scr.bkgd(' ', colors.get('on 232'))

        self.time += 1

        h, w = scr.getmaxyx()
        self.yoffset = 50-h + 15
        scr.addstr(h-1, 0, f'{self.timestr} {self.xoffset:0.0f} +{self.dx:0.1f} {self._status}')

        for y in range(0, h):
            if y < h-16:
                fg, bg, ch = sunset_color(self.time+y*15)
                scr.addstr(y, 0, ch*(w-1), colors.get(f'{fg} on {bg}'))
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
        elif ch in ['l', 'KEY_RIGHT']: self.max_speed = min(self.max_speed+self.incrdx, 4)
        elif ch in ['h', 'KEY_LEFT']: self.max_speed = max(self.max_speed-self.incrdx, 0)
        elif ch in ['k', 'KEY_UP']: self.yoffset -= 3
        elif ch in ['j', 'KEY_DOWN']: self.yoffset += 3
        elif ch in ['KEY_NPAGE']: self.xoffset += 128
        elif ch in ['KEY_PPAGE']: self.xoffset -= 128
        else:
            self.status(f'unknown key {ch}')
