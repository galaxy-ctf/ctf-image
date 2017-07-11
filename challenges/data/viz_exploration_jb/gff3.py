import random
WIDTH = 10

def seq(length, handle):
    handle.write('>ctgA\n')
    for i in range(length):
        handle.write(random.choice(['A', 'C', 'T', 'G']))

BASE_LINE = {
    'source': 'ctgA',
    'exec': 'figlet2gff3',
    'type': 'gene',
    'start': 0,
    'end': 20000,
    'score': 1,
    'strand': '+',
    'phase': '.',
    'attr': {}
}

def header(handle):
    handle.write('##gff-version 3\n')

def pl(handle, line):
    q = [
        line['source'],
        line['exec'],
        line['type'],
        line['start'],
        line['end'],
        line['score'],
        line['strand'],
        line['phase'],
        ';'.join(['%s=%s' % (k, v) for (k, v) in line['attr'].iteritems()])
    ]
    handle.write('\t'.join(map(str, q)) + '\n')

def gene(handle, start, end, idx):
    gene_id = 'g.%s' % idx
    BASE_LINE.update({
        'type': 'gene',
        'start': start,
        'end': end,
        'attr': {'ID': gene_id},
    })
    pl(handle, BASE_LINE)
    return gene_id


def mRNA(handle, gene_id, start, end, j):
    mRNAid = '%s.%02d' % (gene_id, j)
    BASE_LINE.update({
        'type': 'mRNA',
        'start': start,
        'end': end,
        'attr': {
            'Parent': gene_id,
            'ID': mRNAid
        }
    })
    pl(handle, BASE_LINE)
    return mRNAid

def cds(handle, mRNAid, start, end, i, score):
    BASE_LINE.update({
        'type': 'CDS',
        'start': start + (i * 10),
        'end': start + (i * 10) + WIDTH,
        'score': score,
        'attr': {
            'Parent': mRNAid,
            'ID': mRNAid + '.' + str(i),
        }
    })
    pl(handle, BASE_LINE)
