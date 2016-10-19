filename=$(basename "$1")

rm jpg/*

gs -dNumRenderingThreads=4 -dNOPAUSE -sDEVICE=jpeg -sOutputFile=jpg/output-%d.jpg -dJPEGQ=100 -r100 -q $1 -c quit

size="$(pdfinfo -box $1 | grep "Page size")"


stdbuf -oL python compute_max_shrink_size.py "$size" | {
  while IFS= read -r line
  do
    echo "$line"
    margins="$line"
  done 
	
	echo "Margins: $margins"
	output="toprint/${filename}"
	

	pdfjam --trim "$margins" --clip true $1 --outfile shrink.pdf
	pdfjam --nup 2x1 --landscape shrink.pdf --outfile $output

	printf "\
pdfjam --trim \"$margins\" --clip true $1 --outfile shrink.pdf \n \
pdfjam --nup 2x1 --landscape shrink.pdf --outfile $output\n"
	gnome-open $output
}
