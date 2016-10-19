from PIL import Image
import itertools
import numpy as np

from os import listdir
from os.path import isfile, join

import sys
import re

seuil = 50
shrink = 0.2

def get_margins(filename,size):
	img = Image.open(filename)
	pixels = img.load()

	H = float(img.size[1])
	W = float(img.size[0])
	black_x = [i for i,j in itertools.product(range(img.size[0]),range(img.size[1])) if max(pixels[i,j])<seuil ]
	black_y = [j for i,j in itertools.product(range(img.size[0]),range(img.size[1])) if max(pixels[i,j])<seuil ]

	margin_top 		= size[1]* (min(black_y)/H)
	margin_bottom 	= size[1]* (1.0-max(black_y)/H)
	margin_left 	= size[0]* (min(black_x)/W)
	margin_right 	= size[0]* (1.0-max(black_x)/W)
	print "Filename: %s \t %.1fcm %.1fcm %.1fcm %.1fcm" %(filename,margin_top,margin_bottom,margin_left,margin_right)
	
	return (margin_top,margin_bottom,margin_left,margin_right)


def get_max_margin(size):
	mypath = "jpg/"
	pictures = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

	margins = []
	for f in pictures:
		try:
			m = get_margins(f,size)
			margins.append(m)
		except Exception,e:
			print e
	
	margin_table = lambda i: [m[i] for m in margins]

	margin_top 		= np.percentile(margin_table(0), 10) - shrink
	margin_bottom 	= np.percentile(margin_table(1), 10)  - shrink
	margin_left 	= np.percentile(margin_table(2), 10)  - shrink
	margin_right 	= np.percentile(margin_table(3), 10)  - shrink

	maring_shrinked = (margin_top,margin_bottom,margin_left,margin_right)


	print "Results (top,bottom,left,right):"
	print "%.1fcm %.1fcm %.1fcm %.1fcm" %maring_shrinked

	for idx,m in enumerate(margins):
		violation = [maring_shrinked[i]>m[i] for i in range(4)]
		if any(violation):
			s = "%.1fcm %.1fcm %.1fcm %.1fcm" %m
			print "Over shrink for %s \t %s \t %s"%(pictures[idx],str(violation),s)

	print "Configuration (left,bottom,right,top)"
	print "%.1fcm %.1fcm %.1fcm %.1fcm" %(margin_left,margin_bottom,margin_right,margin_top)


def get_pdf_size(info):
	r = re.findall(r'\d+',info)
	pts_to_cm = 0.0352778
	try:
		return (float(r[0])*pts_to_cm,float(r[1])*pts_to_cm)
	except Exception,e:
		print e
		print "Size not found"
		return (29.7,21.0)

if __name__ == '__main__':
	pdf_size = get_pdf_size(sys.argv[1])
	print "Use size: ",pdf_size
	get_max_margin(pdf_size)