#!/opt/local/bin/python

from optparse import OptionParser
import subprocess
import token_util
import glob
import os
import re
import math
import locale

encoding = locale.getdefaultlocale()[1]

parser = OptionParser()
parser.add_option("-g", "--glob", 
				dest="fileglob",
				help="Glob pattern of images to tokenify")

(options, args) = parser.parse_args()


if (options.fileglob is not None):
	words = []

	for f in glob.glob(options.fileglob):
		filenameParts = os.path.splitext(os.path.basename(f))
		filenameBase = filenameParts[0]
		words += filenameBase.split(" ")

	for word in sorted(set(words)):
		print(word) 

else:
	parser.print_help()
	exit(-1)