#!/usr/bin/perl
# -*- Mode: cperl -*-
#--------------------------------------------------------------------------------
# Copyright (C) 2000 by Chmouel Boudjnah <chmouel@mandrakesoft.com>, MandrakeSoft
# Redistribution of this file is permitted under the terms of the GNU 
# Public License (GPL)
#--------------------------------------------------------------------------------
## description: 
# Update a system from inetd file to xinetd.

use strict;

my $inet_files = '/etc/inetd.conf';
my $dir = '/etc/xinetd.d/';
my $remain;
my $choose;

parse_options(@ARGV);
$choose = shift;

die "Need a service to convert\n" if not $choose and not $remain;

system("/bin/mkdir " . "-p " . "$dir") unless -d $dir;

local *F;
open F, $inet_files;
while (<F>) {
    next if /^#/;
    my @t = split;
    my ($service, $socket_type, $protocol, $attente, $user, $server) = split;
    my $programs; $programs .= "$t[$_] " for 6 .. $#t;
    next if -f "$dir/$service";
    next if $service !~ /^$choose$/ and not $remain;
    
    select W; open W, ">$dir/$service";
    print "# Converted by Linux-Mandrake_inetdconvert\n";
    print "service $service\n{\n";
    print "\tsocket_type\t\t= $socket_type\n";
    print "\tprotocol\t\t= $protocol\n";
    print "\twait\t\t\t= ", $attente =~ /yes/ ? "no" : "yes", "\n";
    if ($user =~ /(\w+)\.(\w+)/)  {
	print "\tuser\t\t\t= $1\n";
	print "\tgroup\t\t\t= $2\n";
    } else {
	print "\tuser\t\t\t= $user\n";
    }
    print "\tserver\t\t\t= $server\n";
    print "\tserver_args\t\t= ", $programs, "\n" if $programs;
    print "\tdisable\t\t\t= no\n}\n";
    close W;
}
close F;

sub usage {
    (my $n = $0) =~ s|.*/||g;
    print <<EOF;
Usage: $n -c -d=xinetd-directory -f=inetd-file servie
  
  -c	--convertremaining:	Convert all the remainning service.
  -d	   --directory=DIR:     Specify another xinetd directory.
  -f	 --inetdfiles=FILE:     Specify an another inetd file.
EOF
  exit(0);
}
    
sub parse_options {
    while ($_[0] =~ /^--/ || $_[0] =~ /^-/) {
	$_ = shift;
	if (/-(?-)(directory|d)=([^ \t]+)/) {
	    $dir=$1;
	} elsif (/-(?-)(inetdfiles|f)=([^ \t]+)/){
	    $inet_files=$1;
	} elsif (/-(?-)(convertremaining|c)/){
	    $remain++;
	} elsif (/-(?-)(help|h)/){
	    usage();
	} else {
	    usage();
	}
    }
}

