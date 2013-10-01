#!/opt/local/bin/python

from optparse import OptionParser
import subprocess
import extract
import glob
import os
import re
import math
import locale

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
	extract.extractToPng(options.filename, page, page, "pdfimg")


	# Get list of PNG files
	images = sorted(glob.glob("pdfimg-*.png"))
	if (len(images) % 2 != 0):
		sys.stderr.write("WARNING: Odd Number of Images Extracted (", len(images),". The last image will be ignored")


	tempFile = "masked_token.png"
	it = iter(images)
	for fl1, fl2 in zip(it, it):
		m = re.search('pdfimg-([0-9]+)-([0-9]+)\.png', fl1)
		pageNum = m.group(1)
		origDir = pageNum + "/orig"

		# Create the page directory if it doesn't already exist
		if (not os.path.isdir(pageNum)):
			if (os.path.exists(pageNum)):
				os.remove(pageNum)
			os.mkdir(pageNum)
			os.mkdir(origDir)

		tokenFileName = pageNum + "/token-" + pageNum + "-" + m.group(2) + ".png"
		backTokenFileName = pageNum + "/token-" + pageNum + "-" + m.group(2) + "-0.png"
		frontTokenFileName = pageNum + "/token-" + pageNum + "-" + m.group(2) + "-1.png"

		print ("Merging: ", fl1, " ", fl2)

		# Apply the alpha mask to the base image
		subprocess.call(["composite", "-compose", "copy_opacity", "+matte", fl2, fl1, tempFile])

		# Move original files into orig dir
		os.rename(fl1, origDir + "/" + fl1)
		os.rename(fl2, origDir + "/" + fl2)

		# Split token into well-named file
		subprocess.call(["convert", tempFile, "-crop", "100%x50%", tokenFileName])

		# Rotate and flip the "back" view
		subprocess.call(["convert", backTokenFileName, "-rotate", "180", "-flop", backTokenFileName])

		# Remove any extra border from the images
		subprocess.call(["convert", frontTokenFileName, "-trim", "+repage", frontTokenFileName])
		subprocess.call(["convert", backTokenFileName, "-trim", "+repage", backTokenFileName])

		cmd = subprocess.Popen("identify -ping -format '%W/%H' " + frontTokenFileName, shell=True, stdout=subprocess.PIPE)
		for line in cmd.stdout.readlines():
			line = line.decode(encoding)
			if "/" in line:
				dimensions = line.split("/")
				size = max(int(dimensions[0]), int(dimensions[1]))
				halfSize = math.floor(size / 2)

				size = str(size)
				halfSize = str(halfSize)

				# Make Square Tokens
				subprocess.call(["convert", backTokenFileName, "-background", "none", "-gravity", "center", "-extent", size + "x" + size, backTokenFileName])
				subprocess.call(["convert", frontTokenFileName, "-background", "none", "-gravity", "center", "-extent", size + "x" + size, frontTokenFileName])
				
				# Add background
				# TODO os.chdir()
				subprocess.call(["convert", backTokenFileName, "-alpha", "on",
					"(", "+clone", "-alpha", "Transparent", "-fill", "#FF000050", "-draw", "'circle " + halfSize + "," + halfSize + " " + halfSize + "," + size + "'", ")",
					"-compose", "dst-over", "-composite", backTokenFileName])
				subprocess.call(["convert", frontTokenFileName, "-alpha", "on",
					"(", "+clone", "-alpha", "Transparent", "-fill", "#FF000050", "-draw", "'circle " + halfSize + "," + halfSize + " " + halfSize + "," + size + "'", ")",
					"-compose", "dst-over", "-composite", frontTokenFileName])

				
				# convert  006/token-006-000-0.png  -alpha on  \
			 #         \( +clone -alpha Transparent -fill \#FF000050 -draw 'circle 401,401 401,803' \) \
			 #         -compose dst-over -composite    token.png

				break



	os.remove(tempFile)
