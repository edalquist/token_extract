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
				help="PDF To Parse", metavar="FILE")
parser.add_option("-s", "--start",
                dest="startPage", type="int",
                help="First page to parse images out of (inclusive)")
parser.add_option("-e", "--end",
                dest="endPage", type="int",
                help="Last page to parse images out of (exclusive)")

(options, args) = parser.parse_args()



		# cmd = subprocess.Popen("identify -ping -format '%W/%H' " + frontTokenFileName, shell=True, stdout=subprocess.PIPE)
		# for line in cmd.stdout.readlines():
		# 	line = line.decode(encoding)
		# 	if "/" in line:
		# 		dimensions = line.split("/")
		# 		size = max(int(dimensions[0]), int(dimensions[1]))
		# 		halfSize = math.floor(size / 2)

		# 		size = str(size)
		# 		halfSize = str(halfSize)

		# 		# Make Square Tokens
		# 		subprocess.call(["convert", backTokenFileName, "-background", "none", "-gravity", "center", "-extent", size + "x" + size, backTokenFileName])
		# 		subprocess.call(["convert", frontTokenFileName, "-background", "none", "-gravity", "center", "-extent", size + "x" + size, frontTokenFileName])
				
				# Add background
				# TODO os.chdir()
				# subprocess.call(["convert", backTokenFileName, "-alpha", "on",
				# 	"(", "+clone", "-alpha", "Transparent", "-fill", "#FF000050", "-draw", "'circle " + halfSize + "," + halfSize + " " + halfSize + "," + size + "'", ")",
				# 	"-compose", "dst-over", "-composite", backTokenFileName])
				# subprocess.call(["convert", frontTokenFileName, "-alpha", "on",
				# 	"(", "+clone", "-alpha", "Transparent", "-fill", "#FF000050", "-draw", "'circle " + halfSize + "," + halfSize + " " + halfSize + "," + size + "'", ")",
				# 	"-compose", "dst-over", "-composite", frontTokenFileName])

				
				# convert  006/token-006-000-0.png  -alpha on  \
			 #         \( +clone -alpha Transparent -fill \#FF000050 -draw 'circle 401,401 401,803' \) \
			 #         -compose dst-over -composite    token.png

