from random import choice
from cittyscape import Thing, TextUnit


class Person(Thing):
    heads= list('OÒÓÔÕÖØŌŎŐƟƠǑǾȌȎȪȬȮȰОӦṌṎṐṒỌỎỐỒỔỖỘỚỜợỢộỌọỘỞỠỢ'
        'oòóôõöøōŏőơǒǫǭǿȍȏȫȭȯȱоӧṍṏṑṓọỏốồổỗộớờởỡợₒⱺⲟꝋꝍꭳௐஇⲞꝊꝌ'
        'eèéêëēĕėęěȅȇȩэӭḕḗḙḛḝẹẻẽếềểễệ⒠')
    torsos=list('ǏḬµƷƸƿǐȸȹḭῲῳῴῶῷÝTŢŤŦƬƮȚȾṪṬṮṰMḾṀṂⱮO86|!')
    legs=list('ɅΏλ')
    head_colors = '114 147 158 189 220'.split()
    torso_colors=list(map(str, range(1, 232)))

    @property
    def subthings(self):
        self.head, self.torso, self.leg = map(choice, (self.heads, self.torsos, self.legs))
        self.color_head = choice(self.head_colors)
        self.color_torso = choice(self.torso_colors)
        self.color_leg = str(int(self.color_torso)+1)

        return [
            TextUnit(self.head, 0, 2, color=self.color_head),
            TextUnit(self.torso, 0, 1, color=self.color_torso),
            TextUnit(self.leg, 0, 0, color=self.color_leg),
        ]
