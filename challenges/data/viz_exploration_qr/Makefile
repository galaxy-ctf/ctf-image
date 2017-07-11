data/out.tsv:
	echo '# x y a b c' > data/out.tsv;
	convert -negate png:out.png txt:- | \
		sed 's/[,:()]/\t/g' | \
		awk '(NR>1){print $1,$2,$3,$4,$5}' >> data/out.tsv;
	sed -i 's/ /\t/g' data/out.tsv

clean:
	rm data/out.tsv
