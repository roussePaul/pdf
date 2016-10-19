rm jpg/*


gs -dNumRenderingThreads=4 -dNOPAUSE -sDEVICE=jpeg -sOutputFile=jpg/output-%d.jpg -dJPEGQ=100 -r100 -q $1 -c quit


size="$(pdfinfo -box $1 | grep "Page size")"
echo $size
python compute_max_shrink_size.py "$size"
