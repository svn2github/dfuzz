#!/usr/bin/perl -w
use strict;
package fuzzer;

sub fuzzer{
#if($#ARGV != 2){ die "Usage: $0 infile outfile seed\n"; }

my $infile  = $_[0];
my $outfile = $_[1];
my $seed    = int $_[2];
my $buffer;
my $filesize;
#my $prob = 0.0001;
my $prob = 0.001;

srand( $seed );

open FILE, $infile or die "***Unable to open $infile\n";
binmode FILE;

open OUT, '>'.$outfile or die "***Unable to write to $outfile\n";
binmode OUT;

while( read( FILE, $buffer, 1024*1024 ) ){
   my @in = split(//, $buffer);
   for my $i (0..$#in){
      if( rand() < $prob ){
         print OUT pack('C', sprintf("%d", rand() * 256) );
      }else{
         print OUT $in[$i];
      }
   }
}
close OUT;
close FILE;
}

sub fuzzer1{
#if($#ARGV != 4){ die "Usage: $0 infile outfile start end seed\n"; }

my $infile  = $_[0];
my $outfile = $_[1];
my $start   = hex $_[2];
my $end     = hex $_[3];
my $seed    = int $_[4];
my $buffer;
my $filesize;
my $prob = 0.004;

srand( $seed );

# We read 3 times:
# $start bytes
# $end - $start + 1 bytes
# $filesize - $end - 1 bytes

open FILE, $infile or die "***Unable to open $infile\n";
binmode FILE;
$filesize = -s $infile;

open OUT, '>'.$outfile or die "***Unable to write to $outfile\n";
binmode OUT;

# 1st read
read( FILE, $buffer, $start );
print OUT $buffer;

# 2nd read
read( FILE, $buffer, $end - $start + 1 );
my @in = split(//, $buffer);
for my $i (0..$#in){
   if( rand() < $prob ){
      print OUT pack('C', sprintf("%d", rand() * 256) );
   }else{
      print OUT $in[$i];
   }
}

# 3rd read
read( FILE, $buffer, $filesize );
print OUT $buffer;

close FILE;
close OUT;
}

sub enum1{
#if($#ARGV != 4){ die "Usage: $0 infile outfile start end seed\n"; }

my $infile  = $_[0];
my $outfile = $_[1];
my $start   = hex $_[2];
my $end     = hex $_[3];
my $seed    = int $_[4];
my $buffer;
my $filesize;
#my $prob = 0.004;

#srand( $seed );

# We read 3 times:
# $start bytes
# $end - $start + 1 bytes
# $filesize - $end - 1 bytes

open FILE, $infile or die "***Unable to open $infile\n";
binmode FILE;
$filesize = -s $infile;

open OUT, '>'.$outfile or die "***Unable to write to $outfile\n";
binmode OUT;

# 1st read
read( FILE, $buffer, $start );
print OUT $buffer;

# 2nd read
read( FILE, $buffer, $end - $start + 1 );
if( $end-$start == 0 ){
   print OUT pack('C', sprintf("%d", $seed) );
}elsif( $end-$start == 1){
   # Big endian
   print OUT pack('C', sprintf("%d", $seed % 256) );
   print OUT pack('C', sprintf("%d", $seed / 256) );
}else{
   die "***Max 2 bytes\n";
}

#my @in = split(//, $buffer);
#for my $i (0..$#in){
#   if( rand() < $prob ){
#      print OUT pack('C', sprintf("%d", rand() * 256) );
#   }else{
#      print OUT $in[$i];
#   }
#}

# 3rd read
read( FILE, $buffer, $filesize );
print OUT $buffer;

close FILE;
close OUT;
}

1;
