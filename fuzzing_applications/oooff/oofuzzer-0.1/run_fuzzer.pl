#!/usr/bin/perl
use strict;
require fuzzer;
require fuzzxml;

if($#ARGV != 0 &&
   $#ARGV != 2 ){
   print "Usage: $0 <file_to_be_fuzzed> (start) (end)\n";
   print "Assumes location of soffice.bin is /usr/lib/openoffice/program/soffice.bin\n";
   die;
}

our $ooo = "/usr/lib/openoffice/program/soffice.bin -norestore";

my @a;
@a = split(/\./, $ARGV[0]);
my $ext = $a[$#a];

if(    $ext eq "odt"  ||
       $ext eq "ods"  ||
       $ext eq "odp"  ){
   &xml($ARGV[0], 0);
}elsif($ext eq "docx" ||
       $ext eq "xlsx" ||
       $ext eq "pptx" ){
   &xml($ARGV[0], 1);
}elsif($ext eq "doc" ||
       $ext eq "xls" ||
       $ext eq "ppt" ||
       $ext eq "gif" ||
       $ext eq "tif" ||
       $ext eq "jpg" ||
       $ext eq "png" ){
   &bin($ARGV[0], $ARGV[1], $ARGV[2]);
}

# .doc, .xls, .ppt, .gif, .tif, .png, .jpg
sub bin{
   my ($arg0, $arg1, $arg2) = @_;

   my $file = $arg0;
   my @a;
   @a = split(/\//, $arg0);
   my $filename = $a[$#a];
   my $file_fuzz = "test_".$filename;
   my $line;

   # Initialise crash report
   my $report = $filename.".report";

   if($arg1 ne "" && $arg2 ne ""){
      $report = sprintf("%s_%s_%s.report", $filename, $arg1, $arg2);
   }

   # Initialise crash report
   open REPORT, ">".$report;
   close REPORT;

   for my $seed (0..1000){

#	system("rm .~lock.$file_fuzz#");
        if($arg1 ne "" && $arg2 ne ""){
	   fuzzer::fuzzer1($file, $file_fuzz, $arg1, $arg2, $seed);
        }else{
	   fuzzer::fuzzer($file, $file_fuzz, $seed);
        }
	print ".";
	my $pid = fork();
	if(not defined $pid){
		die "***Unable to fork\n";
	}elsif($pid == 0){
		system("$ooo $file_fuzz");
		#system("$ooo -norestore $file_fuzz");
		my $exit_code = $? >> 8;

                if($exit_code){
		    printf "ooo exited with %d\n", $exit_code;
                    open REPORT, ">>".$report;
                    print REPORT "$filename $seed $exit_code\n";
                    close REPORT;
                }
		exit(0);
	}else{
		sleep(5);
		system("killall -9 soffice.bin");
		#kill 9, $pid;
		#waitpid($pid,0);
	}

	print $seed."\n";
	sleep(2);
   }
   system("rm $file_fuzz");
}

# .odt, .ods, .odp, .docx, .xlsx, .pptx
sub xml{
   my ($arg0, $arg1) = @_;

   my $file = $arg0;
   my @a;
   @a = split(/\//, $arg0);
   my $filename = $a[$#a];
   my $file_fuzz = "test_".$filename;
   my $line;

   # Initialise crash report
   my $report = $filename.".report";

   # Initialise crash report
   open REPORT, ">".$report;
   close REPORT;

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

   for my $seed (0..1000){

      # XML-specific stuff
      if( $#xmls != $#xmls_orig ){
         die "***Something wrong?\n";
      }
      for my $i (0..$#xmls){
         fuzzxml::fuzzxml($xmls_orig[$i], $xml_fuzz, $seed);
         system("cp $xml_fuzz $xmls[$i]");
      }

      chdir $dir;
      if($arg1 == 0){
         system("zip -0 -X ../".$file_fuzz." mimetype");
         system("zip -n .xml -r ../".$file_fuzz." * -x mimetype");
      }else{
         system("zip -n .xml -r ../".$file_fuzz." *");
      }
      chdir "../";


      my $pid = fork();
      if(not defined $pid){
           die "***Unable to fork\n";
      }elsif($pid == 0){
           system("$ooo -minimized -invisible -nologo -norestore $file_fuzz");
           #system("$ooo -norestore $file_fuzz");
           my $exit_code = $? >> 8;

           if($exit_code){
               printf "ooo exited with %d\n", $exit_code;
               open REPORT, ">>".$report;
               print REPORT "$filename $seed $exit_code\n";
               close REPORT;
           }
           exit(0);
      }else{
           sleep(10);
           system("killall -9 soffice.bin");
           #kill 9, $pid;
           #waitpid($pid,0);
      }

      print $seed."\n";
      sleep(2);
   }

   system("rm -rf $dir");
   system("rm $file_fuzz");
   system("rm $xml_fuzz");
   foreach(@xmls_orig){
      system("rm $_");
   }
}

