#!/opt/local/bin/python

from optparse import OptionParser
import extract
import glob

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

	for fl in images:
		print (fl)
	# Sort list
	# Convert pairs of images

	# make image square
	# add background circle, possibly with colors






