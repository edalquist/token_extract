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
parser.add_option("-p", "--prefix", 
				dest="prefix",
				help="New Prefix")

parser.add_option("-d", "--dir", 
				dest="dir",
				help="Base Directory")


(options, args) = parser.parse_args()

if (options.prefix is None):
	parser.print_help()
	exit(-1)

if (options.dir is not None):
	os.chdir(options.dir)

# Make sure we are starting with a clean directory
for img in glob.glob("*/token-*-f.png"):
	print(img + " -> " + )
	#os.rename(fl1, origDir + "/" + fl1)
