#!/opt/local/bin/python

from optparse import OptionParser
import subprocess
import token_util
import glob
import os
import re
import math
import locale
import sys
from wand.image import Image
from wand.display import display

encoding = locale.getdefaultlocale()[1]

parser = OptionParser()
parser.add_option("-f", "--file", 
				dest="filename",
				help="PDF To Parse", metavar="FILE")
parser.add_option("-s", "--start",
                dest="startPage", type="int",
                help="First page to parse images out of (inclusive)")
parser.add_option("-e", "--end",
                dest="endPage", type="int",
                help="Last page to parse images out of (exclusive)")

(options, args) = parser.parse_args()

if (options.filename is None):
	parser.print_help()
	exit(-1)

if (options.startPage is None):
	options.startPage = 1

if (options.endPage is None):
	options.endPage = options.startPage + 1

print ('Parsing PDF', options.filename, 'from', options.startPage, 'to', options.endPage)
for page in range(options.startPage, options.endPage):
	print('Page: ', page)

	# Make sure we are starting with a clean directory
	for img in glob.glob("pdfimg-*.*"):
		os.remove(img)

	token_util.extractToPng(options.filename, page, page, "pdfimg")


	# Get list of PNG files
	images = sorted(glob.glob("pdfimg-*.png"))
	if (len(images) % 2 != 0):
		sys.stderr.write("WARNING: Odd Number of Images Extracted (" + str(len(images)) + ". The last image will be ignored")


	it = iter(images)
	for fl1, fl2 in zip(it, it):
		print fl1
		print fl2
		m = re.search('pdfimg-([0-9]+)-([0-9]+)\.png', fl1)

		pageNum = m.group(1)
		origDir = pageNum + "/orig"
		fullDir = pageNum + "/full"
		frontDir = pageNum + "/front"
		backDir = pageNum + "/back"

		# Create the page directory if it doesn't already exist
		if (not os.path.isdir(pageNum)):
			if (os.path.exists(pageNum)):
				os.remove(pageNum)
			os.mkdir(pageNum)

		if (not os.path.isdir(origDir)):
			os.mkdir(origDir)
		if (not os.path.isdir(fullDir)):
			os.mkdir(fullDir)
		if (not os.path.isdir(frontDir)):
			os.mkdir(frontDir)
		if (not os.path.isdir(backDir)):
			os.mkdir(backDir)

		tokenFileName = pageNum + "/token-" + pageNum + "-" + m.group(2) + ".png"
		backTokenFileName = backDir + "/token-" + pageNum + "-" + m.group(2) + "-back.png"
		frontTokenFileName = frontDir + "/token-" + pageNum + "-" + m.group(2) + "-front.png"
		fullTokenFileName = fullDir + "/token-" + pageNum + "-" + m.group(2) + "-full.png"

		print ("Merging: ", fl1, " ", fl2)

		with Image(filename=fl1) as fullToken:
			with Image(filename=fl2) as mask:
				# Apply the alpha mask to the base image
				fullToken.composite_channel('all_channels', mask, 'copy_opacity', 0, 0)

				# Calcuate the crop data
				cropWidth = fullToken.size[0]
				cropHeight = int(math.floor(fullToken.size[1]/2))
				fullHeight = fullToken.size[1]

				fullToken.save(filename=fullTokenFileName)
	
				with fullToken[0:cropWidth, cropHeight:fullHeight] as tokenFront:
					# Trim excess whitespace
					tokenFront.trim()
					tokenFront.save(filename=frontTokenFileName)

				with fullToken[0:cropWidth, 0:cropHeight] as tokenBack:
					# Trim excess whitespace
					tokenBack.trim()
					tokenBack.rotate(180)
					tokenBack.flop()
					tokenBack.save(filename=backTokenFileName)
				
		# Move original files into orig dir
		os.rename(fl1, origDir + "/" + fl1)
		os.rename(fl2, origDir + "/" + fl2)

	for f in glob.glob("pdfimg-*.*"):
		os.remove(f)