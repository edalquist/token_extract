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
	
	# Remove all ppm files
	for fl in glob.glob("*.ppm"):
		subprocess.call(["mogrify", "-format", "png", fl])
		os.remove(fl)

