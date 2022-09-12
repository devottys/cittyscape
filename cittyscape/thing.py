from dataclasses import dataclass

from .utils import TextUnit



@dataclass
class Subthing:
    x: int=0
    y: int=0
    subt: str=''  # |Thing
    color: str=''  # override subthing colors if specified

    def itertext(self):
        if isinstance(self.subt, TextUnit):
            t = self.subt
            yield TextUnit(t.text, t.x+self.x, t.y+self.y, self.color or t.color)
        elif isinstance(self.subt, str):
            yield TextUnit(self.subt, self.x, self.y, self.color)
        else:
            for t in self.subt.itertext():
                yield TextUnit(t.text, t.x+self.x, t.y+self.y, self.color or t.color)


class Thing:
    def __init__(self, w, h, **kwargs):
        self.w = w
        self.h = h
        self.__dict__.update(**kwargs)

    @property
    def subthings(self):
        'List of Subthing(rel_x, rel_y, Thing|Text, color_override) tuples.'
        return []

    def itertext(self):
        'Generate Subthing.'
        for subt in self.subthings:
            if isinstance(subt, TextUnit):
                yield subt
            else:
                yield from subt.itertext()


class Text(Thing):
    text: str
    color: str = ''

    @property
    def subthings(self):
        return [Subthing(0, 0, self.text, self.color)]
