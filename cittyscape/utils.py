from dataclasses import dataclass
import functools
import string
from random import choice, random
import curses


keycodes = { getattr(curses, k):k for k in dir(curses) if k.startswith('KEY_') }
keycodes.update({chr(i): '^'+chr(64+i) for i in range(32)})

def getkey(scr):
    try:
        ch = scr.get_wch()
        return keycodes.get(ch, ch)
    except curses.error:
        return ''


letters = {
    "funky": 'AB☇DEƑGĦḮJƘLⱮƝ◯☧Q☈S⟙UVW☓Y☡abcdefghijklmnopqrstuvwxyz0123456789',
    "circled": 'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨',
    "fullwidth": 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
    "dotted": 'ȦḂĊḊĖḞĠḢİJKLṀṄȮṖQṘṠṪUVẆẊẎŻȧḃċḋėḟġḣẛjklṁṅȯṗqṙṡṫuvẇẋẏż0123456789',
}

fuzzyfonts = [
        str.maketrans(string.ascii_uppercase+string.ascii_lowercase+string.digits, font)
        for font in letters.values()
    ]

altletters = {
        'A': 'AÀÁÂÃÄÅĀĂĄǍǞǠǺȀȂȦȺАӐӒḀẠẢẤẦẨẪẬẮẰẲẴẶ',
        'B': 'BƁƂɃḂḄḆꞖ',
        'C': 'CÇĆĈĊČƇȻḈꞒꟄ',
        'D': 'DĎĐƊḊḌḎḐḒꟇ',
        'E': 'EÈÉÊËĒĔĖĘĚȄȆȨɆЭӬḔḖḘḚḜẸẺẼẾỀỂỄỆ',
        'F': 'FƑḞꞘ',
        'G': 'GĜĞĠĢƓǤǦǴḠꞠ',
        'H': 'HĤĦȞḢḤḦḨḪⱧꞪ',
        'I': 'IÌÍÎÏĨĪĬĮİƗǏȈȊᵻḬḮỈỊⰋ',
        'J': 'JĴɈꞲ',
        'K': 'KĶƘǨḰḲḴⱩꝀꝂꝄꞢ',
        'L': 'LĹĻĽĿŁȽḶḸḺḼⱠⱢⳐꝈꞭ',
        'M': 'MḾṀṂⱮ',
        'N': 'NÑŃŅŇƝǸȠṄṆṈṊꞐꞤ',
        'O': 'OÒÓÔÕÖØŌŎŐƟƠǑǾȌȎȪȬȮȰОӦṌṎṐṒỌỎỐỒỔỖỘỚỜỞỠỢⲞꝊꝌ',
        'P': 'PƤṔṖⱣꝐꝒꝔ',
        'Q': 'QꝖꝘ',
        'R': 'RŔŖŘȐȒɌṘṚṜṞⱤꝚꞦ',
        'S': 'SŚŜŞŠȘṠṢṤṦṨⱾꞨꟅꟉ',
        'T': 'TŢŤŦƬƮȚȾṪṬṮṰ',
        'U': 'UÙÚÛÜŨŪŬŮŰŲƯǓǕǗǙǛȔȖɄУӮӰӲᵾṲṴṶṸṺỤỦỨỪỬỮỰꞸ',
        'V': 'VƲṼṾꝞ',
        'W': 'WŴẀẂẄẆẈⱲ',
        'X': 'XẊẌ',
        'Y': 'YÝŶŸƳȲɎẎỲỴỶỸỾ',
        'Z': 'ZŹŻŽƵȤẐẒẔⱫⱿꟆ',
        'a': 'aàáâãäåāăąǎǟǡǻȁȃȧаӑӓᶏḁẚạảấầẩẫậắằẳẵặₐ⒜ⱥꬱꭰ',
        'b': 'bƀƃɓᵬᶀḃḅḇ⒝ꞗ',
        'c': 'cçćĉċčƈȼɕḉ⒞ꞓꞔ',
        'd': 'dďđƌȡɖɗᵭᶁᶑḋḍḏḑḓ⒟ꟈ',
        'e': 'eèéêëēĕėęěȅȇȩɇэӭᶒḕḗḙḛḝẹẻẽếềểễệₑ⒠ⱸꬴꭱ',
        'f': 'fƒᵮᶂḟ⒡ꞙ',
        'g': 'gĝğġģǥǧǵɠᶃḡꞡ',
        'h': 'hĥħȟɦḣḥḧḩḫẖₕⱨꞕ',
        'i': 'iìíîïĩīĭįǐȉȋɨиѝӣӥᵢᶖḭḯỉịⁱⰻꭲ',
        'j': 'jĵǰɉʝⱼ',
        'k': 'kķƙǩᶄḱḳḵₖⱪꝁꝃꝅꞣ',
        'l': 'lĺļľŀłƚȴɫɬɭᶅḷḹḻḽₗⱡⳑꝉꞎꬷꬸꬹ',
        'm': 'mɱᵯᶆḿṁṃₘ⒨ⓜꬺ',
        'n': 'nñńņňŉƞǹȵɲɳᵰᶇṅṇṉṋⁿₙꞑꞥꬻ',
        'o': 'oòóôõöøōŏőơǒǫǭǿȍȏȫȭȯȱоӧṍṏṑṓọỏốồổỗộớờởỡợₒⱺⲟꝋꝍꭳ',
        'p': 'pƥᵱᵽᶈṕṗₚꝑꝓꝕ',
        'q': 'qɋʠꝗꝙ',
        'r': 'rŕŗřȑȓɍɼɽɾᵣᵲᵳᶉṙṛṝṟꝛꞧꭇꭉ',
        's': 'sśŝşšșȿʂᵴᶊṡṣṥṧṩₛꞩꟊꮝ',
        't': 'tţťŧƫƭțȶʈᵵṫṭṯṱẗₜⱦ',
        'u': 'uùúûüũūŭůűųưǔǖǘǚǜȕȗʉᵤᶙṳṵṷṹṻụủứừửữựꞹꭎꭏꭒꭴµ',
        'v': 'vʋᵥᶌṽṿⱱⱴꝟꭵ',
        'w': 'wŵẁẃẅẇẉẘⱳ',
        'x': 'xᶍẋẍₓꭖꭗꭘꭙ',
        'y': 'yýÿŷƴȳɏẏẙỳỵỷỹỿꭚ',
        'z': 'zźżžƶȥɀʐʑᵶᶎẑẓẕⱬ',
}

digits = {
  "DIGIT": "0123456789",
  "SUPERSCRIPT": "⁰¹²³⁴⁵⁶⁷⁸⁹",
  "FULLWIDTH": "０１２３４５６７８９",
  "SUBSCRIPT": "₀₁₂₃₄₅₆₇₈₉",
  "CIRCLED": "①②③④⑤⑥⑦⑧⑨⓪",
  "DICE": "⚀⚁⚂⚃⚄⚅",
  "ARABIC-INDIC": "٠١٢٣٤٥٦٧٨٩",
  "EXTENDED ARABIC-INDIC": "۰۱۲۳۴۵۶۷۸۹",
#  "NKO": "߀߁߂߃߄߅߆߇߈߉",
  "DEVANAGARI": "०१२३४५६७८९",
  "BENGALI": "০১২৩৪৫৬৭৮৯",
#  "GURMUKHI": "੦੧੨੩੪੫੬੭੮੯",
#  "GUJARATI": "૦૧૨૩૪૫૬૭૮૯",
#  "ORIYA": "୦୧୨୩୪୫୬୭୮୯",
#  "TAMIL": "௦௧௨௩௪௫௬௭௮௯",
#  "TELUGU": "౦౧౨౩౪౫౬౭౮౯",
#  "KANNADA": "೦೧೨೩೪೫೬೭೮೯",
#  "MALAYALAM": "൦൧൨൩൪൫൬൭൮൯",
#  "SINHALA LITH": "෦෧෨෩෪෫෬෭෮෯",
  "THAI": "๐๑๒๓๔๕๖๗๘๙",
#  "LAO": "໐໑໒໓໔໕໖໗໘໙",
#  "TIBETAN": "༠༡༢༣༤༥༦༧༨༩",
#  "MYANMAR": "၀၁၂၃၄၅၆၇၈၉",
#  "MYANMAR SHAN": "႐႑႒႓႔႕႖႗႘႙",
#  "KHMER": "០១២៣៤៥៦៧៨៩",
#  "MONGOLIAN": "᠐᠑᠒᠓᠔᠕᠖᠗᠘᠙",
#  "LIMBU": "᥆᥇᥈᥉᥊᥋᥌᥍᥎᥏",
#  "NEW TAI LUE": "᧐᧑᧒᧓᧔᧕᧖᧗᧘᧙",
#  "TAI THAM HORA": "᪀᪁᪂᪃᪄᪅᪆᪇᪈᪉",
#  "TAI THAM THAM": "᪐᪑᪒᪓᪔᪕᪖᪗᪘᪙",
#  "BALINESE": "᭐᭑᭒᭓᭔᭕᭖᭗᭘᭙",
#  "SUNDANESE": "᮰᮱᮲᮳᮴᮵᮶᮷᮸᮹",
#  "LEPCHA": "᱀᱁᱂᱃᱄᱅᱆᱇᱈᱉",
#  "OL CHIKI": "᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙",
#  "VAI": "꘠꘡꘢꘣꘤꘥꘦꘧꘨꘩",
#  "SAURASHTRA": "꣐꣑꣒꣓꣔꣕꣖꣗꣘꣙",
#  "KAYAH LI": "꤀꤁꤂꤃꤄꤅꤆꤇꤈꤉",
#  "JAVANESE": "꧐꧑꧒꧓꧔꧕꧖꧗꧘꧙",
#  "MYANMAR TAI LAING": "꧰꧱꧲꧳꧴꧵꧶꧷꧸꧹",
#  "CHAM": "꩐꩑꩒꩓꩔꩕꩖꩗꩘꩙",
#  "MEETEI MAYEK": "꯰꯱꯲꯳꯴꯵꯶꯷꯸꯹",
}

currencies = "$¢£¤¥֏؋߾߿৲৳৻૱௹฿៛₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿꠸﷼﹩＄￠￡￥￦"

def fuzz(s, n=1):
    r = ''
    digitscript = choice(list(digits.keys()))
    letterscript = choice(list(letters.keys()))
    nchanged = 0
    for ch in s:
        if ch == '#':
            ch = choice(digits[digitscript])
        elif ch == '$':
            ch = choice(currencies)
        elif ch == 'X':
            ch = choice(letters[letterscript][0:26])

        if nchanged < n and random() < 0.25:
            r += choice(altletters.get(ch, ch))
            nchanged += 1
        else:
            r += ch
    return r


@dataclass
class TextUnit:
    text: str=''
    x: int=0
    y: int=0
    color: str=''


def hline(abc, x, y, w, color=''):
    a,b,c = abc
    yield TextUnit(a, x, y, color=color) # ML
    for x1 in range(x+1, x+w-1):
        yield TextUnit(b, x1, y, color=color)
    yield TextUnit(c, x+w-1, y, color=color) # MR

def vline(ch, x, y, h, color=''):
    for y in range(y, y+h+1):
        yield TextUnit(ch, x, y, color=color)


class Box:
    def __init__(self, x1=0, y1=0, w=1, h=1):
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h

        self.normalize()

    def __str__(self):
        return f'({self.x1}+{self.w},{self.y1}+{self.h})'

    def normalize(self):
        'Make sure w and h are non-negative, swapping coordinates as needed.'
        if self.w < 0:
            self.x1 += self.w
            self.w = -self.w

        if self.h < 0:
            self.y1 += self.h
            self.h = -self.h

    @property
    def x2(self):
        return self.x1+self.w+1

    @x2.setter
    def x2(self, v):
        self.w = v-self.x1-1
        self.normalize()

    @property
    def y2(self):
        return self.y1+self.h+1

    @y2.setter
    def y2(self, v):
        self.h = v-self.y1-1
        self.normalize()

    def contains(self, b):
        'Return True if this box contains any part of the given x,y,w,h.'
        xA = max(self.x1, b.x1)  # left
        xB = min(self.x2, b.x2)  # right
        yA = max(self.y1, b.y1)  # top
        yB = min(self.y2, b.y2)  # bottom
        return xA < xB-1 and yA < yB-1   # xA+.5 < xB-.5 and yA+.5 < yB-.5


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
        return choice(list(self.colors.keys()))

colors = Colors()
