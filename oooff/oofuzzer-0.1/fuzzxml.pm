#!/usr/bin/perl -w
package fuzzxml;
use strict;
use XML::Parser;
use XML::Writer;
use IO::File;
use Getopt::Long;


my $remove_tag_prob;
my $change_int_prob;
my $remove_attr_prob;
my $copy_attr_value_prob;
my %attr_range;


# -----------------------------------------------------------------------------
sub fuzzxml{
   my $base_prob = 1 / 1000;

   my $infile = shift @_;
   my $outfile = shift @_;
   my $seed = shift @_;

   srand ($seed) if defined $seed;

   $remove_tag_prob = 0.1 * $base_prob;
   $remove_attr_prob = 0.1 * $base_prob;
   $change_int_prob = $base_prob;
   $copy_attr_value_prob = $base_prob;
   %attr_range = ();

# -----------------------------------------------------------------------------

   my $tree;
   {
       my $parser = new XML::Parser ('Style' => 'Tree');
       $parser->setHandlers('Start' => \&MyStart);
       $tree = $parser->parsefile ($infile);
   }

   &study_tags ($tree);
   foreach my $key (sort keys %attr_range) {
       $attr_range{$key} = [sort keys %{$attr_range{$key}}];
   }

   &fuzz_tags ($tree);

   {
       my $f = new IO::File ($outfile, "w");
       my $writer = new XML::Writer(OUTPUT => $f);

       # Take care of utf-8 chars
       binmode($f, ":encoding(utf-8)");
       $writer->xmlDecl("UTF-8");

       &write_xml ($writer, $tree);
   }
}
# -----------------------------------------------------------------------------

sub fuzz_tags {
    my ($pl) = @_;

    for (my $i = 0; $i + 1 < @$pl; $i += 2) {
	my $tag = $pl->[$i];
	my $cont = $pl->[$i + 1];

	if ($tag eq '0') {
	    &fuzz_text (\$cont);
	    $pl->[$i + 1] = $cont;
	} else {
	    if (&doit ($remove_tag_prob)) {
                print "\n";
		splice @$pl, $i, 2;
		$i -= 2; # Counter the add
		next;
	    }

	    my ($attrs,@l) = @$cont;
	    &fuzz_attrs ($attrs);
	    &fuzz_tags (\@l);
	    $pl->[$i + 1] = [$attrs, @l];
	}	
    }
}

sub fuzz_text {
    my ($pt) = @_;
    my $t = ${$pt};

    if (&looks_like_int ($t) && &doit ($change_int_prob)) {
	my $i = int((rand() - 0.5) * 2 * 2147483647);
        print " ".$i."\n";
	${$pt} = $i;
	return;
    }
}

sub fuzz_attrs {
    my ($pa) = @_;

    my @l = @$pa;
    for (my $i = 0; $i + 1 < @l; $i += 2) {
	if (&doit ($remove_attr_prob)) {
            print "\n";
	    splice @l, $i, 2;
	    $i -= 2; # Counter the add
	    next;
	} else {
	    my $attr = $l[$i];
	    my $N = @{$attr_range{$attr}};
	    if ($N > 1 && &doit ($copy_attr_value_prob)) {
		# Copy a random value seen for this attribute.
                my $rand_index = int (rand ($N));
                print " ".$rand_index."\n";
		$l[$i + 1] = $attr_range{$attr}->[$rand_index];
	    } else {
		&fuzz_text (\$l[$i + 1]);
	    }
	}
    }
    @$pa = @l;
}

# -----------------------------------------------------------------------------

sub study_tags {
    my ($pl) = @_;

    for (my $i = 0; $i + 1 < @$pl; $i += 2) {
	my $tag = $pl->[$i];
	my $cont = $pl->[$i + 1];

	if ($tag eq '0') {
	    &study_text ($cont);
	} else {
	    my ($attrs,@l) = @$cont;
	    &study_attrs ($attrs);
	    &study_tags (\@l);
	}	
    }
}

sub study_text {
}

sub study_attrs {
    my ($pa) = @_;

    for (my $i = 0; $i + 1 < @$pa; $i += 2) {
	my $attr = $pa->[$i];
	my $value = $pa->[$i + 1];
	$attr_range{$attr}{$value} = 1;
    }
}

# -----------------------------------------------------------------------------

sub write_xml {
    my ($writer,$pl) = @_;

    for (my $i = 0; $i + 1 < @$pl; $i += 2) {
	my $tag = $pl->[$i];
	my $cont = $pl->[$i + 1];

	if ($tag eq '0') {
	    $writer->characters($cont);
	} else {
	    my ($attrs,@l) = @$cont;
	    if (@l == 0) {
		$writer->emptyTag($tag, @$attrs);
	    } else {
		$writer->startTag($tag, @$attrs);
		&write_xml ($writer, \@l);
		$writer->endTag($tag);
	    }
	}	
    }
}

# -----------------------------------------------------------------------------

sub doit {
    my ($p) = @_;
    if(rand() < $p){
        print "1";
        return 1;
    }

    print "0\n";
    return 0;
#    return rand() < $p;
}

# -----------------------------------------------------------------------------

sub looks_like_int {
    my ($t) = @_;
    return ($t =~ /^[-+]?\d+$/) ? 1 : 0;
}

# -----------------------------------------------------------------------------
# Just like XML::Parse::Style::Tree::start, except attrs as list.

sub MyStart {
  my $expat = shift;
  my $tag = shift;
  my $newlist = [ [ @_ ] ];
  push @{ $expat->{Lists} }, $expat->{Curlist};
  push @{ $expat->{Curlist} }, $tag => $newlist;
  $expat->{Curlist} = $newlist;
}

1;
