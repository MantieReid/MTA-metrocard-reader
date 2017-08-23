#!/usr/bin/python
#
# cab.py: Create Aiken Biphase
# create a WAV file with arbitrary data in it
#
# Copyright(c) 2006, Major Malfunction <majormal@pirate-radio.org>
# http://www.alcrypto.co.uk
#
# inspired by 'dab.c' by Joseph Battaglia <sephail@sephail.net>
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
# version 0.1:
#	just get the thing working with fixed WAV and other parameters!

import wave
import sys
from struct import *
from math import *

if len(sys.argv) < 4:
	print sys.argv[0] + " usage:\n"
	print "\t" + sys.argv[0] + " <output file> <data ('011001')> <frequency> [r]everse"
	print

	sys.exit(-1)

newtrack=wave.open(sys.argv[1],"w")
params= (1, 2, 22050, 0L, 'NONE', 'not compressed')
newtrack.setparams(params)
frequency= int(sys.argv[3]) - 1
data= sys.argv[2]

if len (sys.argv) == 5 and sys.argv[4] == 'r':
	newdata= []
	n= len(data) - 1
	while n >= 0:
		newdata.append(data[n])
		n= n - 1
	data= newdata

peak= 32767

# sinewaves need to be half waves to work - can't be bothered to
# figure it out now!
#slopezero= [0]*frequency
#slopeone= [0]*frequency
#for n in range(frequency):
#	x = n*pi*2/frequency
#	slopezero[n] = eval("sin(x)") * peak
#for n in range(frequency):
#	x = n*pi*2/(frequency / 2)
#	slopeone[n] = eval("sin(x)") * peak

# write some leading silence
for x in range(20):
	newtrack.writeframes(pack("h",0))

# write the actual data
# square wave for now
n= 0
writedata= peak
while n < len(data):
	if data[n] == '1':
		for x in range(2):
			writedata= -writedata
			for y in range(frequency/4):
				newtrack.writeframes(pack("h",writedata))
	if data[n] == '0':
		writedata= -writedata
		for y in range(frequency/2):
			newtrack.writeframes(pack("h",writedata))
	n= n + 1
newtrack.close()
