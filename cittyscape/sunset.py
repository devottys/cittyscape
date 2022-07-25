import math


ttylight_palette = [
                16, 232, 233, 234, 235, 17, 53, 89, 125, 161, 197,
                196,
                202, 208, 214, 215, 216, 217, 182, 147, 111, 75, 39]


def normalise(x, offset=64800, r_min=0, r_max=86400, t_min=0, t_max=2):
    x = (x + offset) % r_max
    normalised_x = (x - r_min) / (r_max - r_min) * (t_max - t_min) + t_min
    return normalised_x


def gradient(y1, y2, x1=(-18), x2=18):
        return (y2 - y1) / (x2 - x1)


def sun_degrees(t, period=90):
    amplitude = normalise(t)
    return math.sin(amplitude * math.pi) * period


def populate(palette):
    ret = []
    for i in range(1, len(palette)):
        for ch in ['\u2593', '\u2592', '\u2591']:
            ret.append((palette[i - 1], palette[i], ch))
    return ret


def sunset_color(t):
    'Return (fg,bg,ch) from 256-color pallette at *t* in seconds since midnight.'
    sun_colors = populate(ttylight_palette)
    m = gradient(0, len(sun_colors) - 1)
    sky_color = math.floor(m*(sun_degrees(t)+18))
    if 0 <= sky_color and sky_color < len(sun_colors):
            return sun_colors[sky_color]
    if sky_color < 0:
            return ttylight_palette[0], ttylight_palette[0], '\u2588'
    if sky_color >= len(sun_colors):
            return ttylight_palette[-1], ttylight_palette[-1], '\u2588'
