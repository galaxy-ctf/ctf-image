import random
import sys
from Bio.Seq import Seq
from Bio import SeqIO

muts = open('mutations', 'r').read()
seqs = SeqIO.parse('genome.fa', 'fasta')
len_seqs = 44
# for each sequence, stuff in FIVE mutations.
for i, seq in enumerate(seqs):
    # Generate five muts, in order
    newseq = list(str(seq.seq))
    sys.stderr.write(''.join(newseq)+ '\n')
    for j in range(5):
        # Pick a random position
        pos = (5 * i) + j
        sys.stderr.write("%s\n" % pos)
        if pos >= len(muts) - 1:
            continue

        mut_val = muts[pos]
        while True:
            mut_pos = 20 + (j * 10) + random.randint(0, 5)
            sys.stderr.write(' ' * mut_pos + mut_val + '\n')
            if newseq[mut_pos] != mut_val:
                newseq[mut_pos] = mut_val
                break
    seq.seq = Seq(''.join(newseq))
    sys.stderr.write(''.join(newseq)+ '\n')
    SeqIO.write([seq], sys.stdout, 'fasta')
