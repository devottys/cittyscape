from random import choice

from cittyscape import Thing, Subthing, TextUnit, Person, Building

centerline_spacing = 3
block_spacing = 250

crosswalkcolor = '246' #'142'
curbcolor1 = '246' #'142'
curbcolor2 = '238' #'58'
streetcolor = '234'
centerlinecolor = '226'


class Street(Thing):
    @property
    def subthings(self):
        def hline(x1, x2, y, ch, color):
            for i in range(x1, x2):
                yield Subthing(i, y, TextUnit(ch, color=color))

        sh = 10  # crosswalk width
        yield from hline(0, self.w, 7, '▇', f'{streetcolor} on {curbcolor1}')
        yield from hline(0, self.w, 8, '▃', f'{curbcolor2} on {streetcolor}')
        yield from hline(0, self.w, 2, '▃', f'{curbcolor2} on {streetcolor}')
        yield from hline(0, self.w, 1, '▇', f'{streetcolor} on {curbcolor1}')

        yield from hline(0, self.w, 6, ' ', f'{centerlinecolor} on {streetcolor}')
        yield from hline(0, self.w, 4, ' ', f'{centerlinecolor} on {streetcolor}')
        yield from hline(0, self.w, 3, ' ', f'{centerlinecolor} on {streetcolor}')

        yield from hline(0, self.w, 5, ' ', f'{centerlinecolor} on {streetcolor}')

        for i in range(0, self.w, centerline_spacing):
            yield Subthing(i, 5, TextUnit('‗', color=f'{centerlinecolor} on {streetcolor}'))

        yield from hline(2, 1+sh, 1, ' ', f'{curbcolor1} on {streetcolor}')
        yield from hline(3, 2+sh, 2, ' ', f'{curbcolor1} on {streetcolor}')
        yield from hline(7, 7+sh, 7, ' ', f'{curbcolor1} on {streetcolor}')
        yield from hline(8, 8+sh, 8, ' ', f'{curbcolor1} on {streetcolor}')

        color = f'{crosswalkcolor} on {streetcolor}'
        for i in range(0, 9):
            yield Subthing(i, i, TextUnit('╱', color=color))
            yield Subthing(i+sh, i, TextUnit('╱', color=color))
            yield from hline(i+1, i+sh, i, ' ', f'{curbcolor1} on {streetcolor}')


class CittyBlock(Thing):
    @property
    def subthings(self):
        # Generate Buildings and Street from the block
        x = 0
        laststreetx = 0
        bldgs = []
        while x < self.w:
            bldgw = choice(list(range(7, 20)) + [23,26,30])
            bldgh = choice(list(range(4, self.h//2)) + [self.h*3//4, self.h*4//5]*3)

            yield Subthing(x, 10+choice((1,1,1,2)), Building(w=bldgw, h=bldgh))

            w = bldgw + choice((-2, -2, -2, -1, -1, 0, 0, 1, 1, 2))
            x += w

            if x - laststreetx > block_spacing:
                yield Subthing(laststreetx, 0, Street(w=x-laststreetx, h=10))
                laststreetx = x
                x += 20

        # people after buildings and street
        x = 0
        for i in range(1000):
            x += choice((2,2,2,3,4,5,6,15,20,25,30,35,40))
            y = choice((0,1, 8, 7, 9))
            yield Subthing(x, y, Person(w=2, h=3))

