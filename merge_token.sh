#!/bin/bash

# Composites Images
# $1 - mask
# $2 - image
# $3 - output

TMP_IMG='composite_temp.png'

composite -compose copy_opacity +matte $1 $2 $TMP_IMG
convert $TMP_IMG -crop 100%x50% $3.png
rm $TMP_IMG
convert  $3-0.png -rotate 180 -flop $3-0.png 
