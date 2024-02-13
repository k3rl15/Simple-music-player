from random import randint


def colors(r, g, b):
    color_increment = randint(3, 6)

    if r == 255 and g < 255 and b == 0:
        g += color_increment
    elif r > 0 and g == 255 and b == 0:
        r -= color_increment
    elif r == 0 and g == 255 and b < 255:
        b += color_increment
    elif r == 0 and g > 0 and b == 255:
        g -= color_increment
    elif r < 255 and g == 0 and b == 255:
        r += color_increment
    elif r == 255 and g == 0 and b > 0:
        b -= color_increment

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return r, g, b
