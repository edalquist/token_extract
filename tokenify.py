#!/opt/local/bin/python

from optparse import OptionParser
import subprocess
import token_util
import glob
import os
import re
import math
import locale
from wand.image import Image
from wand.display import display

encoding = locale.getdefaultlocale()[1]

parser = OptionParser()
parser.add_option("-f", "--file", 
				dest="filename",
				help="Image to tokenify", metavar="FILE")
parser.add_option("-d", "--dest", 
				dest="basedir",
				help="Base directory to save tokenified images to")
parser.add_option("-g", "--glob", 
				dest="fileglob",
				help="Glob pattern of images to tokenify")

(options, args) = parser.parse_args()

if (options.filename is not None):
	token_util.tokenify(options.filename, basedir=options.basedir)

elif (options.fileglob is not None):
	for f in glob.glob(options.fileglob):
		token_util.tokenify(f, basedir=options.basedir)

else:
	parser.print_help()
	exit(-1)
