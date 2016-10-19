#left, bottom, right and top
pdfjam --trim "$2" --clip true $1 --outfile shrink.pdf
pdfjam --nup 2x1 --landscape shrink.pdf --outfile output.pdf
