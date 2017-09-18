#/usr/bin/bash
#
# Decode MTA MetroCard Raw And Parsed Data
# Version 1.1
# Written in 2017 by Linxin <.>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Notes on input:
# A line that begins with a '#' is not processed and not printed
# A line that begins with a '%' is printed as a comment
#
clear


while true; do
clear

echo ""
echo ""
echo "                                    #######################################"
echo "                                   #                                       #"
echo "                                   # STANDER ISO CARD Decoding System V1.1 #"
echo "                                   #       Written in 2017 by Linxin       #"
echo "                                   #                                       #"
echo "                                    #######################################"
echo ""
echo ""
echo ""
echo ""
echo ""
read -n 1 -s -p "Press any key to Read..."
echo ""
python rcd.py
python dab.py metrocard.wav
python dab.py metrocard.wav | python dmsb.py dmsb
read -n 1 -s -p "Press any key to read next card..."
done
