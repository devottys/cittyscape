from typing import Sequence
from itertools import product
from random import choice

from wcwidth import wcswidth

from .utils import fuzz, Box, Text


class Thing:
    def __init__(self,
                 style:Sequence[str],
                 box:Sequence[Box],
                 color:Sequence[str]=['']):
        # choose a random style for the thing, and a constrained random box that it will fit in. also a random color.

        styles = style if isinstance(style, (list, tuple)) else [style]
        boxes = box if isinstance(box, (list, tuple)) else [box]
        colors = color if isinstance(color, (list, tuple)) else [color]

        fits = []
        for style, box in product(styles, boxes):
            lines = style.splitlines()

            if len(lines) <= box.h and max(map(wcswidth, lines or [''])) <= box.w:
                fits.append((style, box))

        if fits:
            self.style, self.box = choice(fits)
        else:
            self.style, self.box = '', boxes[0]

        # fuzz text
        if self.style.isascii():
            self.style = fuzz(self.style)

        self.lines = self.style.splitlines()
        self.color = choice(colors)

    def __iter__(self):
        if not self.lines:
            return
        x1 = self.box.x1
        y1 = self.box.y1

        dy = range(0, self.box.h-len(self.lines))
        if dy:
            y1 += choice(dy)

        dx = range(0, self.box.w-wcswidth(self.lines[0]))
        if dx:
            x1 += choice(dx)

        for linenum, line in enumerate(self.lines[::-1]):
            x = x1
            for ch in line:
                yield Text(ch, x, y1-linenum, color=self.color)
                x += wcswidth(ch)

    def sub(self, cls, dx, dy, w, h, color=''):
        if dx < 0:
            x = self.box.x2+dx
        else:
            x = self.box.x1+dx

        if dy < 0:
            y = self.box.y2+dy+1
        else:
            y = self.box.y1+dy
        return cls(Box(x, y, w, h), color=color)


    def subthing(self, text, dx, dy, w, h, color=''):
        if dx < 0:
            x = self.box.x2+dx
        else:
            x = self.box.x1+dx

        if dy < 0:
            y = self.box.y2+dy+1
        else:
            y = self.box.y1+dy
        return Thing(text, Box(x,y,w,h), color=color)


