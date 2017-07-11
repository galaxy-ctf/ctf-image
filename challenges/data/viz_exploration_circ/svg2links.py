import sys
import xml.etree.ElementTree
from math import atan2, degrees

# Invoke as 'python script.py '
e = xml.etree.ElementTree.parse(sys.argv[1]).getroot()[1]
CHROM = sys.argv[2]
CHROM_SIZE = int(sys.argv[3])

for line in e:
    # <line stroke="#000000" stroke-opacity="0.501961" x1="196.734288"
    # y1="235.979617" x2="125.645322" y2="255.978340" stroke-width="1" />
    score = int(line.attrib['stroke'].replace('#', '0x'), 16)
    b = score & 255
    g = score >> 8 & 255
    r = score >> 16 & 255
    # Get avg value + map to (0, 1000)
    score = 1000 * float(r + g + b) / (3 * 255)

    x1 = float(line.attrib['x1']) - 125
    y1 = float(line.attrib['y1']) - 125
    x2 = float(line.attrib['x2']) - 125
    y2 = float(line.attrib['y2']) - 125

    a1 = (int(CHROM_SIZE * (degrees(atan2(y1, x1)) + 180) / 360) - (CHROM_SIZE / 4)) % CHROM_SIZE
    a2 = (int(CHROM_SIZE * (degrees(atan2(y2, x2)) + 180) / 360) - (CHROM_SIZE / 4)) % CHROM_SIZE

    print("%s %s %s %s %s %s value=%s" % (CHROM, a1, a1, CHROM, a2, a2, score))
