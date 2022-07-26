import functools
import random
import curses


keycodes = { getattr(curses, k):k for k in dir(curses) if k.startswith('KEY_') }
keycodes.update({chr(i): '^'+chr(64+i) for i in range(32)})


def getkey(scr):
    try:
        ch = scr.get_wch()
        return keycodes.get(ch, ch)
    except curses.error:
        return ''


class Colors:
    def __init__(self):
        self.color_pairs = {}  # (fgcolornum, bgcolornum) -> pairnum
        self.colors = {x[6:]:getattr(curses, x) for x in dir(curses) if x.startswith('COLOR_') and x != 'COLOR_PAIRS'}

    @functools.lru_cache(None)
    def get(self, colorstr):
        attrs = 0
        fgbg = [7, 232]
        i = 0
        for x in colorstr.split():
            if x == 'on': i = 1
            elif attr := getattr(curses, 'A_' + x.upper(), None):
                attrs |= attr
            else:
                fgbg[i] = int(x) if x.isdigit() else self.colors.get(x.upper(), 0)

        pairnum = self.color_pairs.get(tuple(fgbg), None)
        if not pairnum:
            pairnum = len(self.color_pairs)+1
            curses.init_pair(pairnum, *fgbg)
            self.color_pairs[tuple(fgbg)] = pairnum
        return curses.color_pair(pairnum) | attrs

    def random(self):
        return random.choice(list(self.colors.keys()))

colors = Colors()
