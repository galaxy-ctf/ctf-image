#!/bin/bash
flag='gccctf{dont_be_a_square}'
for (( i=0; i<${#flag}; i++  )); do
	char="${flag:$i:1}"
	if [ ! -f "svgs/$char.svg" ]; then

		../../../logo/text-to-svg "${flag:$i:1}" > $char.a.svg
		../../../logo/node_modules/.bin/svgexport $char.a.svg $char.a.png png 100% 500:
		rm $char.a.svg
		convert -flatten -gravity center -extent 1000x1000 $char.a.png $char.png
		rm -f "$char.a.png"
		# Convert to SVG links.
		./main -i "$char.png" -j 8 -m 9 -o "svgs/$char.svg" -n 1000 -v
		rm -f "$char.png"
	fi
	## Now convert to links file.

	chr_name=$(cat karyotype.human.hg38.txt | awk "(NR==1 + $i){print \$3}")
	chr_size=$(cat karyotype.human.hg38.txt | awk "(NR==1 + $i){print \$6}")
	echo $char $i $chr_name $chr_size
	outname="$i.txt"
	if [ $i -lt 10 ]; then
		outname="0$outname"
	fi
	python svg2links.py "svgs/$char.svg" $chr_name $chr_size > data/$outname
	grep "$chr_name " karyotype.human.hg38.txt > data/karyotype.$chr_name.txt


	cp data/karyotype.$chr_name.txt circos/data/karyotype.txt
	cp data/$outname circos/data/links.txt
	docker run -it -v `pwd`/circos:/input erasche/circos
	cp circos/circos.png $i.png
done
