from render import render_text
from gff3 import mRNA, cds, seq, gene, header

FLAG = "gccctf{data_designer}".upper()

with open('out.fa', 'w') as handle:
    seq(20000, handle)

SPACING = 100
WIDTH = 150
THRESH = 255

import sys
handle = sys.stdout

for idx, char in enumerate(list(FLAG)):
    header(handle)
    img_resized = render_text(char)
    start = idx * WIDTH + (idx * SPACING)
    end = (idx + 1) * WIDTH + (idx * SPACING)

    (img_width, img_height) = img_resized.size
    gene_idx = gene(handle, start, end, idx)
    for y in range(img_height):
        mRNAid = mRNA(handle, gene_idx, start, end, y)

        for x in range(img_width):
            (r, g, b, a) = img_resized.getpixel((x, y))
            if r > THRESH and g > THRESH and b > THRESH:
                continue

            score = 1 - (float(r) + float(g) + float(b)) / (3 * 255)
            cds(handle, mRNAid, start, end, x, score)
