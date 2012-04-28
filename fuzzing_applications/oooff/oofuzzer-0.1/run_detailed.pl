#!/usr/bin/perl
use strict;
require fuzzer;
require fuzzxml;

if($#ARGV != 1 ){
   print "Usage: $0 <file> <report>\n";
   die;
}

our $ooo = "/usr/lib/openoffice/program/soffice.bin";

my @a;
@a = split(/\./, $ARGV[0]);
my $ext = $a[$#a];

if(    $ext eq "odt"  ||
       $ext eq "ods"  ||
       $ext eq "odp"  ){
   &xml_d($ARGV[0], $ARGV[1], 0);
}elsif($ext eq "docx" ||
       $ext eq "xlsx" ||
       $ext eq "pptx" ){
   &xml_d($ARGV[0], $ARGV[1], 1);
}elsif($ext eq "doc" ||
       $ext eq "xls" ||
       $ext eq "ppt" ||
       $ext eq "gif" ||
       $ext eq "tif" ||
       $ext eq "jpg" ||
       $ext eq "png" ){
   &bin_d($ARGV[0], $ARGV[1]);
}

# .doc, .xls, .ppt, .gif, .tif, .png, .jpg
sub bin_d{
   my ($arg0, $arg1) = @_;

   my $file = $arg0;
   my @a;
   @a = split(/\//, $arg0);
   my $filename = $a[$#a];
   my $file_fuzz = "test_".$filename;
   my $line;

   my $report_file = $arg1;
   @a = split(/\//, $arg1);
   my $report_filename = $a[$#a];

   # Make gdb autorun
   open FILE, ">.gdbinit";
   print FILE "set logging on\n";
   print FILE "run -norestore -nologo -invisible -minimized $file_fuzz\n";
   print FILE "x/i \$eip\n";
   print FILE "info reg\n";
   close FILE;

   # Initialise crash report
   my $report = $filename.".detailed";
   my $start = "";
   my $end = "";

   @a = split(/\./, $report_filename);
   $report_filename = $a[$#a-1];
   @a = split(/_/, $report_filename);
   if($#a >= 2 &&
      $a[$#a-1] !~ /[A-Z,g-z]/ &&
      $a[$#a] !~ /[A-Z,g-z]/ ){
      $start = '0x'.$a[$#a-1];
      $end = '0x'.$a[$#a];
      $report = sprintf("%s_%s_%s.detailed", $filename, $a[$#a-1], $a[$#a] );
   }

   # Initialise crash report
   open REPORT, ">".$report;
   close REPORT;

   my $inline;
   open INFILE, $arg1;
   while( $inline = <INFILE> ){
      #if( substr($inline, 0, 1) ne ' ' ){
      if( $inline =~ /^[0-9,a-z,A-Z]/ ){
         my @b = split(/ /, $inline);
         my $seed = $b[1];

         # Clear contents of gdb.txt
         open FILE, ">gdb.txt";
         close FILE;

#       system("rm .~lock.$file_fuzz#");
         if($start eq ""){
            fuzzer::fuzzer($file, $file_fuzz, $seed);
         }else{
            fuzzer::fuzzer1($file, $file_fuzz, $start, $end, $seed);
         }
         system("gdb $ooo&");

         sleep(15);
#        system("killall -9 gdb");
         system("killall -9 soffice.bin");

         if(open FILE, "gdb.txt"){
                while($line = <FILE>){
                        if($line =~ /SIGSEGV/){
                                open REPORT, ">>".$report;
                                print REPORT "$filename $seed SEGV\n";

                                for my $j (1..12){
                                        my $line2 = <FILE>;
                                        print REPORT "   ".$line2;
                                }
                                print REPORT "\n";
                                close REPORT;
                                last;
                        }
                }
                close FILE;
         }
         print $seed."\n";
         sleep(3);
       }
   }
   close INFILE;

   #clean up
   system("rm $file_fuzz");
}

# .odt, .ods, .odp, .docx, .xlsx, .pptx
sub xml_d{
   my ($arg0, $arg1, $arg2) = @_;

   my $file = $arg0;
   my @a;
   @a = split(/\//, $arg0);
   my $filename = $a[$#a];
   my $file_fuzz = "test_".$filename;
   my $line;

   my $report_file = $arg1;
   @a = split(/\//, $arg1);
   my $report_filename = $a[$#a];

   # Make gdb autorun
   open FILE, ">.gdbinit";
   print FILE "set logging on\n";
   print FILE "run -norestore -nologo -invisible -minimized $file_fuzz\n";
   print FILE "x/i \$eip\n";
   print FILE "info reg\n";
   close FILE;

   # Initialise crash report
   my $report = $filename.".detailed";

   # Initialise crash report
   open REPORT, ">".$report;
   close REPORT;
   my ($arg0) = @_;

   # XML-specific stuff
   my $dir = "test";
   my @xmls;
   my @xmls_orig;
   my $xml_fuzz = "test.xml";
   system("unzip -d $dir $file");
   system("find $dir/ -name \\*.xml -print > xml_list");
   open XML_LIST, "xml_list" or die "***Unable to open xml_list\n";
   @xmls = <XML_LIST>;
   close XML_LIST;
   system("rm xml_list");
   foreach(@xmls){
      my $a = $_;
      chomp $a;
      chomp $a;
      my @b = split(/\//, $a);
      #print $b[$#b]."\n";
      push(@xmls_orig, $b[$#b]);
      system("cp $a ".$b[$#b]);
   }
   if( $#xmls != $#xmls_orig ){
      die "***Something wrong?\n";
   }

   my $inline;
   open INFILE, $arg1;
   while( $inline = <INFILE> ){
      #if( substr($inline, 0, 1) ne ' ' ){
      if( $inline =~ /^[0-9,a-z,A-Z]/ ){
         my @b = split(/ /, $inline);
         my $seed = $b[1];

         # Clear contents of gdb.txt
         open FILE, ">gdb.txt";
         close FILE;

         # XML-specific stuff
         for my $i (0..$#xmls){
            fuzzxml::fuzzxml($xmls_orig[$i], $xml_fuzz, $seed);
            system("cp $xml_fuzz $xmls[$i]");
         }

         chdir $dir;
         if($arg2 == 0){
            system("zip -0 -X ../".$file_fuzz." mimetype");
            system("zip -n .xml -r ../".$file_fuzz." * -x mimetype");
         }else{
            system("zip -n .xml -r ../".$file_fuzz." *");
         }
         chdir "../";

         system("gdb $ooo&");
         sleep(15);
#         system("killall -9 gdb");
         system("killall -9 soffice.bin");

         if(open FILE, "gdb.txt"){
                while($line = <FILE>){
                        if($line =~ /SIGSEGV/){
                                open REPORT, ">>".$report;
                                print REPORT "$filename $seed SEGV\n";

                                for my $j (1..12){
                                        my $line2 = <FILE>;
                                        print REPORT "   ".$line2;
                                }
                                print REPORT "\n";
                                close REPORT;
                                last;
                        }
                }
                close FILE;
         }
         print $seed."\n";
         sleep(3);
      }
   }
   close INFILE;

   #clean up
   system("rm -rf $dir");
   system("rm $file_fuzz");
   system("rm $xml_fuzz");
   foreach(@xmls_orig){
      system("rm $_");
   }
}

