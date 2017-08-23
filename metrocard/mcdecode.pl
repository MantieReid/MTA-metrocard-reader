#!/usr/bin/perl
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
# Linxin 2017
# wulinxin304115735@gmail.com
#
# Notes on input:
# A line that begins with a '#' is not processed and not printed
# A line that begins with a '%' is printed as a comment
#


$card_type = 0; #FIXME: this should be set by track 3, but since I only have
 # a single-track reader...
$typesfile = '/Users/wulinxin/Desktop/metrocard/types.txt';
$lidfile = '/Users/wulinxin/Desktop/metrocard/lids.txt';
# track 1-2 field names
@T12_FIELDS = (
 'Time', 'Sub-Type', 'Time', 'Date',
 'Times Used', 'Expiration', 'Transfer', 'Last ID',
 'Value', 'Purch ID', 'Unknown'
);


# track 3 field names
@T3_FIELDS = (
 'Type', 'Unknown', 'Expiration', 'Unkonwn',
 'Unknown', 'Unknown', 'Serial', 'Unused',
 'Unkonwn', 'Constant'
);
# generate regexps for track 1-2
@t12_lens = (2, 6, 6, 10, 6, 10, 1, 15, 16, 16); # lengths of track 1-2 fields
$t12_re1 = '11010111'; # start sentinel
$t12_re1 .=     join('', map("([01]{$_})", @t12_lens)); # track 1-2 fields
$t12_re2 .= $t12_re1 . '(.*)' . $t12_re1; # regexp for dual records
# generate regexp for track 3
@t3_lens = (4, 4, 12, 4, 8, 8, 80, 16, 16); # lengths of track 3 fields
$t3_re = '000011000111'; # start sentinel

$t3_re = '000000110001'; # start sentinel

$t3_re .= join('', map("([01]{$_})", @t3_lens)); # track 3 fields
$t3_re .= '0010010100110010011010010110010101001100101001'; # end sentinel
$t3_re .= '0100110011010101001101001010100110100101011010';

# lookup card type/subtype in typesfile and return its name
sub lookup_type($$)
{
 ($in_type, $in_subtype) = @_; # read arguments
 open(FH, $typesfile) or die "Can't open $typesfile: $!"; # open typesfile
 while (<FH>) { # loop through each record
 ($type, $subtype, $name) = split(/:/); # split fields
 if (($type eq $in_type) and ($subtype eq $in_subtype)) { # look for match
 chomp($name); # remove newline
 return $name; # return name
 return $subtype
 }
 }
 return 'UNKNOWN'; # could not find type/subtype; return 'UNKNOWN'
}
# lookup last id in lidfile and return its name
sub lookup_lid($)
{
 ($in_value) = @_; # read arguments
 open(FH, $lidfile) or die "Can't open $lidfile: $!"; # open lidfile
 while (<FH>) { # loop through each record
 ($value, $name) = split(/:/); # split fields
 if (($in_value eq $value)) { # look for match
 chomp($name); # remove newline
 return $name; # return name
 }
 }
 return 'UNKNOWN'; # could not find lid; return 'UNKNOWN'
}
# print header
sub print_header($)
{
 ($title) = @_; # read arguments
 print("$title\n"); # print title
 print("     Field         Hex       Decimal  Parsed\n"); # print header
 print("--------------- ---------- ---------- ------\n");
}
# print field as hex and decimal and return decimal value
sub print_field($$$)
{
 ($track, $field, $value) = @_; # read arguments
 $tvar = 'T' . $track . '_FIELDS'; # create variable name
 $value = oct('0b' . $value); # convert to decimal
 printf('%2d: %-11s ', $field, $$tvar[$field - 1]);
 printf('%10X %10d ', $value, $value); # print base 10/16 values
 return $value; # return decimal value
}
# parse field
sub parse_field($$$)
{
 ($track, $field, $value) = @_; # read arguments
 $decvalue = oct('0b' . $value);

 if ($track == 12) { # track 1-2 fields

 if ($field == 1 or $field == 3) { # time
 if ($card_type == 0) {
 $time = $decvalue * 6;
 $hr = int($time / 60) - 1;
 $min = $time % 60;
 printf("%.2d:%.2d", $hr, $min);
 }
 }

 if ($field == 2) { # subtype
 print(lookup_type($card_type, $decvalue));
 }

 if ($field == 5) { # times used
 print($decvalue);
 }

 if ($field == 7) { # transfer
 print(($decvalue == 1) ? "YES" : "NO");
 }

 if ($field == 8) { # last id
 print(lookup_lid($decvalue));
 }

 if ($field == 9) { # value
 $dollars = int($decvalue / 100);
 $cents = $decvalue % 100;
 printf("\$%d.%.2d", $dollars, $cents);
 }
 }

 if ($track == 3) { # track 3 fields

 if ($field == 1) { # type
 print(lookup_type('M', $decvalue));
 $card_type = $decvalue;
 }

 if ($card_type == 0 and $field == 3) { # expiration
 $day = 30;
 if (!$decvalue % 2) {
 $decvalue++;
 }
 $decvalue /= 2;
 my $year = int ($decvalue / 12) + 1992;
 my $month = $decvalue % 12;
 if ($month > 1) {
 $month--;
 }
 else {
 $year--;
 $month = 12;
 }
 if ($month < 8) {
 if ($month % 2) {
 $day = "31";
 }
 }
 else {
 if (!($month % 2)) {
 $day = "31";
 }
 }
 if ($month == 2) {
 if (!($year % 4)) {
 $day = 29;
 }
 else {
 $day = 28;
 }
 }
 print("$month/$day/$year");
 }

 if ($field == 7) { # serial
 printf("%.10d", $decvalue);
 }
 }

 print("\n");
}
# main loop
while (<STDIN>) {

 if (/^%(.*)/) { # process printed comments
 print("### $1\n"); # print
 next; # process next input line
 }
 if (/^#/) { # process ignored comments
 next; # process next input line
 }

 # track 3
 if (/$t3_re/ or reverse =~ /$t3_re/) {
 print_header 'Track 3 Record';
 for ($i = 1; $i <= ($#t3_lens + 2); $i++) {
 $field = $i; # set field
 print_field(3, $field, $$i); # print each field
 parse_field(3, $field, $$i); # parse each field
 }
 print "\n";
 }

 # track 1-2 dual records
 if (/$t12_re2/ or reverse =~ /$t12_re2/) { # regexp
 print_header 'Track 1-2 Record 1'; # print header
 for ($i = 1; $i <= ($#t12_lens + 2); $i++) {
 $field = $i; # set field
 print_field(12, $field, $$i); # print/parse each field
 if ($field == 1 or $field == 3) { # time field is split in two
 parse_field(12, $field, $1 . $3); # combine time fields
 }
 else { # everything else is normal
 parse_field(12, $field, $$i); # parse each field
 }
 }
 print "\n";
 print_header 'Track 1-2 Record 2'; # print header
 for ($i = ($#t12_lens + 3); $i <= (($#t12_lens * 2) + 4); $i++) {
 $field = $i - ($#t12_lens + 2); # set field
 print_field(12, $field, $$i); # print/parse each field
 if ($field == 1 or $field == 3) { # time field is split in two
 $timevar1 = ($#t12_lens + 3);
 $timevar2 = ($#t12_lens + 5);
 parse_field(12, $field, $$timevar1 . $$timevar2); # combine time fields
 }
 else { # everything else is normal
 parse_field(12, $field, $$i); # parse each field
 }
 }
 print "\n";
 next; # process next input line
 }

 # track 1-2 single record
 if (/$t12_re1/ or reverse =~ /$t12_re1/) { # regexp
 print_header 'Track 1-2 (Read Error)'; # print header
 for ($i = 1; $i <= ($#t12_lens + 2); $i++) {
 $field = $i; # set field
 print_field(12, $field, $$i); # print each field
 if ($field == 1 or $field == 3) { # time field is split in two
 parse_field(12, $field, $1 . $3); # combine time fields
 }
 else { # everything else is normal
 parse_field(12, $field, $$i); # parse each field
 }
 }
 print "\n";
 next; # process next input line
 }
}
