import sys

from PIL import Image

symbol_table = [
    '@',
    '#',
    '&',
    '(',
    '%',
    '/',
    '*',
    '~',
    ',',
    '.',
    ' '
]

def clamp(v, inf=0, inl=255, outf=0, outl=len(symbol_table)-1):
    # i = int(((v - inf) / (inl - inf)) * (outl - outf) + outf)
    i = int((v / inl) * outl)
    return i

def get_symbol(v, use_table=True):
    if use_table:
        i = clamp(v)
        return symbol_table[i]
    else:
        i = clamp(v, outf=33, outl=126) #int(((v - 0) / (255 - 0)) * (126 - 33) + 33)
        return chr(i)

def main():
    infilename = sys.argv[1]
    mono_outfilename = "mono.png"
    ascii_outfilename = "ascii.txt"
    
    target_w = 0
    target_h = 0

    with Image.open(infilename) as image: 
        pixels = image.load()
        width, height = image.size

        target_w = 400

        target_h = int(((height * target_w) / width) / 2)
        print(target_w, target_h)
        symbols = [[0 for x in range(target_w)] for y in range(target_h)]        

        for x in range(width):
            for y in range(height):
                x1 = clamp(x, 0, width, 0, target_w)
                y1 = clamp(y, 0, height, 0, target_h)
                # print(x1, y1)
                c = pixels[x,y]
                m = int((c[0] + c[1] + c[2]) / 3)
                # m = 255 - m
                pixels[x,y] = (m, m, m)
                symbols[y1][x1] = get_symbol(m, True)
        image.save(mono_outfilename)

        with open(ascii_outfilename, 'w+') as f:
            for y in symbols:
                for x in y:
                    f.write(f"{x}")
                f.write("\n")


if __name__ == "__main__": 
    main() 