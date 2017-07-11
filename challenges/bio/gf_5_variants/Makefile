all: calls.bcf

mutations:
	echo 'gccctf{dc4194cc-8ad2-4781-95e1-7a296689866e}' | \
		xxd -b -c 1 | \
		awk '{print $$2}' | \
		sed 's/\(..\)\(..\)\(..\)\(..\)/\1\n\2\n\3\n\4/g' | \
		sed 's/00/G/g;s/01/A/g;s/10/T/g;s/11/C/g' | \
		tr -d '\n' > mutations

genome.mod.fa: mutations
	python mod.py genome.fa > genome.mod.fa

single.sam: genome.mod.fa
	./art_bin_MountRainier/art_illumina -ss HS25 -ef -sam -i genome.mod.fa -l 100 -f 40 -o single;

# Provide to users.
single.bam: single.sam
	samtools-1.5/samtools sort single_errFree.sam -o single.bam

# "Solving the problem"
calls.bcf: single.bam
	./bcftools/bcftools mpileup -f genome.fa single.bam | ./bcftools/bcftools call -mv -Ob -o calls.bcf
	bcftools/bcftools view calls.bcf;

distrib: calls.bcf
	mkdir -p distribute

clean:
	rm -f single.bcf single.bam single.sam single.aln single_dat.fq single.fq \
		single_dat.aln single_dat.sam calls.bcf single_errFree.sam *.fai *.bai
