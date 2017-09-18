#!/usr/bin/python
# 
# cmsb.py: Create MagStripe Binary
# Convert ASCII data to ABA/IATA binary with LRC
# Inspired by dmsb.c by Joseph Battaglia <sephail@sephail.net>
# 
# Copyright 2006,2007 Major Malfunction <majormal@pirate-radio.org>
# version 0.1 (IATA only)
#   http://www.alcrypto.co.uk/
#   Distributed under the terms of the GNU General Public License v2
# version 0.2 (add ABA capability, characterset checking)
#   Parts Copyright 2007 Mansour Moufid <mmoufid@connect.carleton.ca>
#   Distributed under the terms of the GNU General Public License v3

import sys
import string
from operator import *

if len(sys.argv) < 3:
	print "cmsb.py v0.2"
	print "Usage: %s <TRACK No.> <DATA> [PADDING]" % sys.argv[0]
	sys.exit(False)

data = sys.argv[2]
if int(sys.argv[1]) == 1:
	bits = 7
	base= 32
	max= 63
elif int(sys.argv[1]) == 2 or int(sys.argv[1]) == 3:
	bits = 5
	base= 48
	max= 15
zero = ''
lrc = []
for x in range(bits):
	zero += "0"
	lrc.append(0)
output = ''

padding = 0
if len(sys.argv) == 4:
	padding = int(sys.argv[3])

for x in range(padding):
	output += zero

for x in range( len(data) ):
	raw = ord(data[x]) - base
	if raw < 0 or raw > max:
		print 'Illegal character:', chr(raw+base)
		sys.exit(False)
	parity = 1
	for y in range(bits-1):
		output += str(raw >> y & 1)
		parity += raw >> y & 1
		lrc[y] = xor(lrc[y], raw >> y & 1)
	output += chr((parity % 2) + ord('0'))

parity = 1
for x in range(bits - 1):
	output += chr(lrc[x] + ord('0'))
	parity += lrc[x]
output += chr((parity % 2) + ord('0'))

for x in range(padding):
	output += zero

print output
