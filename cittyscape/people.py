from random import choice
from cittyscape import *


class Person(Thing):
    heads='ợ Ợ ộ Ọ ọ Ộ ௐ இ'.split()
    torsos='Ǐ Ḭ µ Ʒ Ƹ ƿ ǐ ȸ ȹ ḭ ῲ ῳ ῴ ῶ ῷ Ý'.split()
    legs='Ʌ Ώ λ'.split()
    colors=list(map(str, range(1, 232)))

    def __init__(self, box):
        self.box = box
        self.head, self.torso, self.leg = map(choice, (self.heads, self.torsos, self.legs))
        self.color_head = choice('114 147 158 189 220'.split())
        # ('58 65 94 100 130 136 142 166 172 178 181 179 214 226 222 230'.split()))
        self.color_torso = choice(self.colors)
        self.color_leg = str(int(self.color_torso)+1)

    def __iter__(self):
        box = self.box
        yield Text(self.head, box.x1, box.y1, color=self.color_head)
        yield Text(self.torso, box.x1, box.y1+1, color=self.color_torso)
        yield Text(self.leg, box.x1, box.y1+2, color=self.color_leg)


def iter_people(h=50):
    x = 0
    for i in range(1000):
        x += choice((2,2,2,3,4,5,6,15,20,25,30,35,40))
        y = h-choice((0,1, -8, -7, -9))
        yield Person(Box(x, y, 2, 3))
