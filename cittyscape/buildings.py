import string
from functools import partial
from random import choice, random

from wcwidth import wcswidth

from .utils import fuzz, hline, vline
from cittyscape import Thing, Subthing, TextUnit


centerline_spacing = 3
block_spacing = 250

crosswalkcolor = '246' #'142'
curbcolor1 = '246' #'142'
curbcolor2 = '238' #'58'
streetcolor = '234'
centerlinecolor = '226'


doors = ['⎡⏉⎤', '⎡|⎤', '┌─╥─┐\n│⠰╫⠆│', '┌─┐\n│⠂│', '⩎', '⫙', '⹑ ⹐ ', 'Ω', '∏', 'ᑍ', 'ᑎ', 'ᑏ', '⟤⟥'] # '⋒'


retail_signs = [
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
retail_signs += '⚢  ⛇  ⛏ ⛑ ⛤  ⛩ ⛯    ✆ ✠ ✡ ➿'.split()
#retail_signs += "Wolf Waag Kerk Faam Juni Boas Lucas Wyers Uilen Arcam Roest Alysa Snoek Maart Vishal Vogels Winkel Europa Burcht Casino Subway Danzig Spanje Italië Helios Hirsch Afrika Titania Douglas Mentrum Hofkerk Cinétol Vyfhoek Rusland Candida".split()


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
    rooftoppers = '𐀀 𐀇 𐀣 𐀵 𐰼'.split()

    def __init__(self, w, h, **kwargs):
        super().__init__(w, h, **kwargs)
        self.floorh = choice(list(range(3, 5)))
        self.closedwintype = choice(self.windowtypes)
        self.maxww = 1
        self.color = choice(self.bldgcolors)

        self.winwidth = choice([2,3,4] if self.maxww == 1 else [2])  # number of contiguous windows
        self.style = choice(list(self.styles))

        self.windy = self.floorh//2
        if self.floorh > 2:
            self.windy -= choice(list(range(self.floorh-2)))

    def place_random(self, x, y, txt, color):
        remain_w = self.w-wcswidth(txt)-x-4
        if remain_w > 1:
            x += choice(range(remain_w))
        yield Subthing(x, y, TextUnit(txt, color=color))

    @property
    def subthings(self):
        # abbc
        # j  k
        # deef
        # j  k
        # ghhi

        a,b,c,d,e,f,g,h,i,j,k = self.style
        floorh = self.floorh

        extrah = (self.h % floorh)
        x2 = self.w-1
        y1 = 0
        y2 = self.h-1
        h = self.h-extrah

        for y in range(y1, y1+self.h):
            yield from hline('   ', 0, y, self.w, color=self.color)

        # edges of building
        yield from vline(j, 0, y1, self.h, color=self.color)
        yield from vline(k, x2, y1, self.h, color=self.color)

        # entry level
        yield from hline((g, ' ', i), 0, 0, self.w, color='underline '+self.color)

        if random() < .75:
            yield from self.place_random(1, 1, fuzz(choice(retail_signs)), color=self.color+' bold')

        yield from self.place_random(0, 0, choice(doors), color=self.color+' bold')

        for floornum, y in enumerate(range(y1, y2+floorh-2, floorh)):
            if floornum > 0:
                yield from hline((d,e,f), 0, y, self.w, color=self.color)
                yield from self.Windows(y)

        # roof
        roofcolor = self.color
        roofcolor += ' underline'
        rooftopper = choice(self.rooftoppers)
        yield from hline((a,b,c), 0, self.h, self.w, color=roofcolor)
        yield Subthing(choice(range(0, self.w-1)), self.h, rooftopper, color=roofcolor)

    def Windows(self, y):
        ww = self.maxww
        for x in range(2, self.w-self.winwidth-ww, self.winwidth*ww):
            for x1 in range(0, self.winwidth-ww, ww+1):
                wincolor = choice(self.wincolors)
                winch = self.closedwintype
                yield Subthing(x+x1, y-self.windy, TextUnit(winch, color=wincolor))
