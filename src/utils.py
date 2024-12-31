import pygame
from pygame import Color
from typing import Union, Tuple, Sequence

ColorValue = Union[Color, int, str, Tuple[int, int, int], Tuple[int, int, int, int], Sequence[int]]

def underlineText(text):
    return f"\033[4m{text}\033[0m"

def boldText(text):
    return f"\033[1m{text}\033[0m"

def printRed(*args, **kwargs):
    print(f"\033[91m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printGreen(*args, **kwargs):
    print(f"\033[92m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printYellow(*args, **kwargs):
    print(f"\033[93m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printPurple(*args, **kwargs):
    print(f"\033[95m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printCyan(*args, **kwargs):
    print(f"\033[96m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printBlue(*args, **kwargs):
    print(f"\033[94m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printOrange(*args, **kwargs):
    print(f"\033[38;5;208m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printGray(*args, **kwargs):
    print(f"\033[90m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printBold(*args, **kwargs):
    print(f"\033[1m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printUnderline(*args, **kwargs):
    print(f"\033[4m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printItalic(*args, **kwargs):
    print(f"\033[3m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def printStrike(*args, **kwargs):
    print(f"\033[9m", end="")
    print(*args, **kwargs)
    print(f"\033[0m", end="")

def formatRed(text):
    return f"\033[91m{text}\033[0m"

def formatGreen(text):
    return f"\033[92m{text}\033[0m"

def formatYellow(text):
    return f"\033[93m{text}\033[0m"

def formatPurple(text):
    return f"\033[95m{text}\033[0m"

def formatCyan(text):
    return f"\033[96m{text}\033[0m"

def formatBlue(text):
    return f"\033[94m{text}\033[0m"

def formatOrange(text):
    return f"\033[38;5;208m{text}\033[0m"

def formatGray(text):
    return f"\033[90m{text}\033[0m"

def formatBold(text):
    return f"\033[1m{text}\033[0m"

def formatUnderline(text):
    return f"\033[4m{text}\033[0m"

def formatItalic(text):
    return f"\033[3m{text}\033[0m"

def formatStrike(text):
    return f"\033[9m{text}\033[0m"

def tint_image(surface: pygame.Surface, color: ColorValue) -> pygame.Surface:
    '''Tint the color of the given image. This is an inplace operation.

    Args:
        surface (pygame.Surface): The image to be tinted. 
        color (ColorValue): The target color.

    Returns:
        pygame.Surface: A surface that is the tinted image.
    '''
    w, h = surface.get_size()
    r, g, b, = color[0], color[1], color[2]
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))