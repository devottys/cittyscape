from random import choice
import random
import string
from functools import partial

from .utils import fuzz, Text, hline, vline, Box
from .thing import Thing

from wcwidth import wcswidth

centerline_spacing = 3
block_spacing = 250

crosswalkcolor = '246' #'142'
curbcolor1 = '246' #'142'
curbcolor2 = '238' #'58'
streetcolor = '234'
centerlinecolor = '226'

def iter_buildings(startblock:int, endblock:int, h:int=50):
    'Generate Buildings from the block'
    x = 0
    laststreetx = 0
    bldgs = []
    startblock -= startblock % 256
    for codepoint in range(startblock, endblock, 16):
#        if codepoint % 256 == 0:
#            random.seed(codepoint)

        bldgw = choice(list(range(7, 20)) + [23,26,30])
        bldgh = choice(list(range(4, h//2)) + [h*3//4, h*4//5]*3)

        box = Box(x, h-bldgh-choice((1,1,1,2)), bldgw, bldgh)
        yield Building(box, address=f'{codepoint//16:2X}')

        w = bldgw + choice(range(-1, 7))
        x += w

        if x - laststreetx > block_spacing:
            yield Street('', Box(laststreetx, h, x-laststreetx, 10))
            laststreetx = x
            x += 20


def Door(box, color=''):
    return Thing(['⎡⏉⎤', '⎡|⎤', '┌─╥─┐\n│⠰╫⠆│', '┌─┐\n│⠂│',
    '⩎', '⫙', '⹑ ⹐ ', 'Ω', '∏', 'ᑍ', 'ᑎ', 'ᑏ', '⟤⟥', # '⋒', 
], box, color)


def Retail(box, color=''):
    return Thing([
    'ラーメン\nRA-MEN',
    'boba\ntea',
    '(.).)',
    '☘ pub ☚',
    '∫o⨏t\nware',
    'PIZZA\n $#',
    'IKEA',
    '¡taco!',
    'View\n ##',
    'Ventana',
    'Park\nside',
    '☣ ☢ ☠ ⚠',
    '♠ ♡\n♢ ♣',

    '### X St',
    'XX ####',
    'XXXX',
    'Kaupþing',
    '☕',  # coffee
    '☊', # headphones
    '☪', # mosque
    '☸', # buddhist temple
    '♫ ოůšīċ ♪',
    'hodl ₿',
    '♬·¯·♩¸♪·¯·♫¸¸',
    "Vicky's\nSecrets",
    '99¢',
    '⚽ ⛹ ⚾\n YMCA',
    'pet\nshop',
    'pawsitive',
    'flowers\n✻✽❁⚘❃❉✿❋',
    '⚣ ሾ',
    '℞ ⚕',  # apothecary
    'баня\n  ♨',  # banya
    '✐ ✉',
    '⛟  ✈ ⛴ ⛍ ',
    '✂ barber ✂',
    '☂ ☂ ☂'
    '⚡ ⚧\ndance'
    ]
    + '⚢  ⛇  ⛏ ⛑ ⛤  ⛩ ⛯    ✆ ✠ ✡ ➿'.split()
    + "Wolf Waag Kerk Faam Juni Boas Lucas Wyers Uilen Arcam Roest Alysa Snoek Maart Vishal Vogels Winkel Europa Burcht Casino Subway Danzig Spanje Italië Helios Hirsch Afrika Titania Douglas Mentrum Hofkerk Cinétol Vyfhoek Rusland Candida".split()
    , box, color)

extrachars = '⛔ '
def Rooftop(box, color):
    return Thing('𐀀 𐀇 𐀣 𐀵 𐰼'.split(), box, color)

class Building(Thing):
    styles = [
        '  .├┄┤│_│┊┆',
        '┌─┐├┄┤│_│┊┆',
        '┏━┓┣┅┫┃_┃┇┋',
        '┍━┑┝┉┥│_│┊┆',
        '┎─┒┠┈┨┃_┃╏╏',
        '╭─╮├╌┤│_│╎╎',
        '╔═╗╠╧╣║_║║║',
    ]
    bldgcolors = ('23', '94', '100', '130', '142', '179', '241')
    wincolors = ['240']*100 + ['250']*10 + ['18', '22', '52', '236', '127']
    windowtypes = '■ ☐ □ ▢ ▣ ▤ ▥ ▦ ▧ ▨ ▩ ▪ ▫ ▬ ▭ ▮ ▯ ◈ ○ ◌ ◍ ◎ ☖ ⊞ ⊟ ⊠ ⌂ ⌑ ⌗ 𐄘 ☰ ☷ 🁣 ▥ 𐧃 ⯐ '.split()
    retailcolors = '21 46 51 93 121 161 180 190 212 226'.split()

    def __init__(self, box, address=''):
        self.address = address
        self.floorh = choice(list(range(3, 5)))
        self.closedwintype = choice(self.windowtypes)
        addr = int(address, 16)
        self.wintypes = []
        self.maxww = 0
        for x in range(addr, addr+16):
            ww = wcswidth(chr(x))
            if ww > 0:
                self.maxww = max(self.maxww, ww)
                self.wintypes.append(chr(x))
        if not self.wintypes:
            self.wintypes = [' ']
            self.maxww = 1

        self.winwidth = choice([2,3,4] if self.maxww == 1 else [2])  # number of contiguous windows
        super().__init__('', box, color=self.bldgcolors)
        self.style = choice(list(self.styles))

        self.windy = self.floorh//2
        if self.floorh > 2:
            self.windy -= choice(list(range(self.floorh-2)))

    def __iter__(self):
        # abbc
        # j  k
        # deef
        # j  k
        # ghhi

        a,b,c,d,e,f,g,h,i,j,k = self.style
        box = self.box
        floorh = self.floorh

        extrah = (box.h % floorh)
        box.y1 += extrah
        y1 = box.y1+1
        box.h -= extrah

        for y in range(y1, y1+box.h):
            yield from hline('   ', box.x1, y, box.w, color=self.color)

        # edges of building
        yield from vline(j, box.x1, y1, box.h, color=self.color)
        yield from vline(k, box.x2-2, y1, box.h, color=self.color)

        for floornum, y in enumerate(range(box.y2, y1, -floorh)):
            if floornum == 0:  # entry level
                yield from hline((g, ' ', i), box.x1, y, box.w, color='underline '+self.color)

                doorx = choice(range(box.w-5))+1
                if doorx < 3:
                    addrx = box.w-4
                else:
                    addrx = 1

                yield from self.Windows(y-1)
                if random.random() < .75:
                    yield from self.sub(Retail, 2, -2, box.w-4, 2, color=self.retailcolors)
                yield from self.sub(Door, doorx, -1, box.w-doorx-4, 2, color=self.color+' bold')
#                yield Text(self.address, box.x1+addrx, y-1, color=self.color+' bold')

            else:  # middle floor
                yield from hline((d,e,f), box.x1, y, box.w, color=self.color)

                yield from self.Windows(y)


        # roof
        roofcolor = self.color + ' underline'
        yield from hline((a,b,c), box.x1, box.y1, box.w, color=roofcolor)
        yield from self.sub(Rooftop, 1, 0, box.w-1, 2, color=roofcolor)

    def Windows(self, y):
        ww = self.maxww
        for x in range(self.box.x1+2, self.box.x2-self.winwidth-ww, self.winwidth*ww):
            for x1 in range(0, self.winwidth-ww, ww+1):
                wincolor = choice(self.wincolors)
                winch = self.closedwintype
                yield Text(winch, x+x1, y-self.windy, color=wincolor)



class Street(Thing):
    def __iter__(self):
        # intersection
        sh = 10
        for i in range(self.box.w):
            if i % centerline_spacing == 0 and (i < 4 or i > sh+4):
                yield from self.subthing('‗', i, 5, 1, 1, color=f'{centerlinecolor} on {streetcolor}')
            else:
                yield from self.subthing(' ', i, 5, 1, 1, color=f'{centerlinecolor} on {streetcolor}')

            yield from self.subthing(' ', i, 4, 1, 1, color=f'{centerlinecolor} on {streetcolor}')
            yield from self.subthing(' ', i, 6, 1, 1, color=f'{centerlinecolor} on {streetcolor}')
            yield from self.subthing(' ', i, 7, 1, 1, color=f'{centerlinecolor} on {streetcolor}')

            if i < 7 or i > sh+7:
                yield from self.subthing('▇', i, 3, 1, 1, color=f'{streetcolor} on {curbcolor1}')
            else:
                yield from self.subthing(' ', i, 3, 1, 1, color=f'{curbcolor1} on {streetcolor}')
            if i < 8 or i > sh+7:
                yield from self.subthing('▃', i, 2, 1, 1, color=f'{curbcolor2} on {streetcolor}')
            else:
                yield from self.subthing(' ', i, 2, 1, 1, color=f'{curbcolor1} on {streetcolor}')
            if i < 3 or i > sh+2:
                yield from self.subthing('▃', i, 8, 1, 1, color=f'{curbcolor2} on {streetcolor}')
            else:
                yield from self.subthing(' ', i, 8, 1, 1, color=f'{curbcolor1} on {streetcolor}')
            if i < 2 or i > sh+1:
                yield from self.subthing('▇', i, 9, 1, 1, color=f'{streetcolor} on {curbcolor1}')
            else:
                yield from self.subthing(' ', i, 9, 1, 1, color=f'{curbcolor1} on {streetcolor}')

            color = f'{crosswalkcolor} on {streetcolor}'
            if i < sh:
                yield from self.subthing('╱', i, sh-i, 1, 1, color=color)
                if i > 0:
                    yield from self.subthing(' ', i, sh, 1, 1, color=f'{curbcolor1} on {streetcolor}')
            elif i < sh*2:
                yield from self.subthing('╱', i, sh*2-i, 1, 1, color=color)
                if i > sh-1 and i < sh*2-1:
                    yield from self.subthing(' ', i, 1, 1, 1, color=f'{curbcolor1} on {streetcolor}')
