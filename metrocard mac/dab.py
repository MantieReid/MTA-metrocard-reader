#!/usr/bin/python

import wave
import sys
from struct import *
from operator import *

if len(sys.argv) < 2:
        print sys.argv[0] + " usage:\n"
        print "\t" + sys.argv[0] + " <WAV file> [%age silence threshold (33)]"
	print
	sys.exit(False)

if len(sys.argv) == 3:
	thresh= 100 / int(sys.argv[2])
else:
	thresh= 100 / 33

track=wave.open(sys.argv[1])
params=track.getparams()
frames=track.getnframes()
channels=track.getnchannels()

if not channels == 1:
	sys.stderr.write("track must be mono!")
	sys.exit(False) 

sys.stderr.write("chanels: " + str(channels))
sys.stderr.write("\nbits: " + str(track.getsampwidth() * 8))
sys.stderr.write("\nsample rate: " + str(track.getframerate()))
sys.stderr.write("\nnumber of frames: " + str(frames))
sys.stderr.write("\n")

n= 0
max= 0
samples= []

# determine max sample and build sample list
while n < frames:
	n += 1
	# make sample an absolute value to simplify things later on
	current= abs(unpack("h",track.readframes(1))[0])
	if current > max:
		max= current 
	samples.append(current)

# set silence threshold
silence= max / thresh
sys.stderr.write("silence threshold: " + str(silence))
sys.stderr.write("\n")

# create a list of distances between peak values in numbers of samples
# this gives you the flux transition frequency

peak= 0
ppeak= 0
peaks= []

n= 0
while n < frames:
	ppeak= peak
	# skip to next data
	while n < frames and samples[n] <= silence:
		n= n+1
	peak= 0
	# keep going until we drop back down to silence
	while n < frames and samples[n] > silence:
		if samples[n] > samples[peak]:
			peak= n
		n= n+1
	# if we've found a peak, store distance
	if peak - ppeak > 0:
		peaks.append(peak - ppeak)
	
sys.stderr.write("max: " + str(max))
sys.stderr.write("\n")

# read data - assuming first databyte is a zero
# a one will be represented by two half-frequency peaks and a zero by a full frequency peak
# ignore the first two peaks to be sure we're past leading crap
zerobl = peaks[2]
n= 2
# allow some percentage deviation
freq_thres= 60
output= ''
while n < len(peaks) - 1:
	if peaks[n] < ((zerobl / 2) + (freq_thres * (zerobl / 2) / 100)) and peaks[n] > ((zerobl / 2) - (freq_thres * (zerobl / 2) / 100)):
		if peaks[n + 1] < ((zerobl / 2) + (freq_thres * (zerobl / 2) / 100)) and peaks[n + 1] > ((zerobl / 2) - (freq_thres * (zerobl / 2) / 100)):
			output += '1'
			zerobl= peaks[n] * 2
			n= n + 1
	else:
		 if peaks[n] < (zerobl + (freq_thres * zerobl / 100)) and peaks[n] > (zerobl - (freq_thres * zerobl / 100)):
			output += '0'
			zerobl= peaks[n]
	n= n + 1		
sys.stderr.write("number of bits: " + str(len(output)))
sys.stderr.write("\n")
print output
