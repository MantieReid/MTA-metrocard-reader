#!/usr/bin/python
#
# dtk23.py: Decode Track2/3 Binary
#
# Copyright(c) 2007, Major Malfunction <majormal@pirate-radio.org>
# http://www.alcrypto.co.uk
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to
#   deal in the Software without restriction, including without limitation the
#   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#   sell copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#   IN THE SOFTWARE.
#

import sys
import string
from operator import *

if len(sys.argv) < 2:
	print sys.argv[0] + " usage:\n"
	print "\t" + sys.argv[0] + " <data ('011001')> [r]everse"
	print

	sys.exit(-1)

data= sys.argv[1]
if len(sys.argv) == 3 and sys.argv[2] == 'r':
	newdata= ''
	n= len(data) - 1
	while n >= 0:
		newdata += data[n]
		n= n - 1
	data= newdata

# check for TK2 or TK3 data - find start sentinel
start_decode= data.find("11010")
if start_decode < 0:
	print "no start sentinel found!"
	sys.exit(-1)
end_sentinel= data.find("11111")
# check end sentinel is on 5 bit boundry
while (end_sentinel - start_decode) % 5:
	newpos= data[end_sentinel + 1:].find("11111")
	if newpos >= 0:
		end_sentinel += newpos + 1
	else:
		print "no end sentinel found!"
		sys.exit(-1)
# LRC comes immediately after end sentinel
actual_lrc= end_sentinel + 5
# initialise rolling LRC
rolling_lrc= [0,0,0,0,0]
decoded_string= ''
# do the decode
while start_decode <= end_sentinel:
	asciichr= 48
	parity= int(data[start_decode + 4])
	for x in range(4):
		asciichr += int(data[start_decode + x]) << x
		parity += int(data[start_decode + x])
		rolling_lrc[x]= xor(rolling_lrc[x],int(data[start_decode + x]))
	# check parity
	if not parity % 2:
		print "parity error!"
		sys.exit(-1)
	decoded_string += chr(asciichr)
	start_decode += 5	
# check LRC
parity= 1
for x in range(4):
	parity += rolling_lrc[x]
rolling_lrc[4]= parity % 2
for x in range(5):
	if not rolling_lrc[x] == int(data[actual_lrc + x]):
		print "LRC/CRC check failed!"
		sys.exit(-1)
print decoded_string
