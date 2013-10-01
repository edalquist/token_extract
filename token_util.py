#!/opt/local/bin/python
import subprocess
import glob
import os

def extractToPng(filename, start, end, imgPrefix):
	if (end is None):
		end = start

	if (imgPrefix is None):
		imgPrefix = "pdfimg"
	
	print ("Extracting pages ", start, "to", end, "from", filename)
	subprocess.call(["pdfimages", "-j", "-p", "-f", str(start), "-l", str(end), filename, imgPrefix])
	
	images = glob.glob(imgPrefix + "-*.*")
	cmd = ["mogrify", "-format", "png"] + images
	subprocess.call(cmd)

	# Remove all extracted image files
	for fl in images:
		os.remove(fl)

