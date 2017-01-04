#!/opt/local/bin/python
import subprocess
import glob
import os
import re
import math
import locale
from wand.image import Image
from wand.display import display


def extractToPng(filename, start, end, imgPrefix):
	if (end is None):
		end = start

	if (imgPrefix is None):
		imgPrefix = "pdfimg"
	
	print "Extracting pages " + str(start) + "to" + str(end) + "from" + filename
	subprocess.call(["pdfimages", "-j", "-p", "-f", str(start), "-l", str(end), filename, imgPrefix])
	
	images = glob.glob(imgPrefix + "-*.*")
	cmd = ["mogrify", "-format", "png"] + images
	subprocess.call(cmd)

	# Remove all extracted image files
	for fl in images:
		os.remove(fl)


def tokenify(filename, overwrite=False, basedir=None):
	with Image(filename=filename) as token:
		width = token.size[0]
		height = token.size[1]
		resize = max(height, width)
		left = int((resize - width) / 2)
		top = int((resize - height) / 2)

		with Image(width=resize, height=resize, ) as squareToken:
			# Copy original image into new image
			squareToken.composite(image=token, left=left, top=top)

			# Calculate save file name
			if (overwrite or basedir is not None):
				saveFilename = filename
			else:
				dirName = os.path.dirname(filename)
				filenameParts = os.path.splitext(os.path.basename(filename))
				filenameBase = filenameParts[0]
				filenameExt = filenameParts[1]
				saveFilename = dirName + "/" + filenameBase + ".square" + filenameExt

			if (basedir is not None):
				if (not basedir.endswith("/")):
					basedir += "/"
				saveFilename = basedir + saveFilename

			print("Resizing '" + filename + "' to " + str(resize) + "px with offsets l" + str(left) + " t" + str(top) + " saving to '" + saveFilename + "'")

			# make sure parent dirs exist
			os.makedirs(os.path.dirname(saveFilename), exist_ok=True)

			# Save the squared token
			squareToken.save(filename=saveFilename)

