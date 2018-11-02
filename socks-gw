#!/usr/bin/perl
# Dave Hansen - August 2013
use strict;
my ($host, $port) = @ARGV;

my $SOCKS5_PROXY = 'proxy-socks.jf.intel.com:1080';
# This will resolve if the local dns search path has the site's
# domain ("search jf.intel.com"), which is the most common case.
if (defined gethostbyname('proxy-socks')) {
	$SOCKS5_PROXY = 'proxy-socks:1080';
}
# Let this be overridden by an environment variable:
$SOCKS5_PROXY = $ENV{SOCKS5_PROXY} if defined $ENV{SOCKS5_PROXY};

(my $SOCKS5_SERVER = $SOCKS5_PROXY) =~ s/:.*//;
(my $SOCKS5_PORT   = $SOCKS5_PROXY) =~ s/.*://;

sub which
{
	my $cmd = shift;
	foreach my $dir (split(":", $ENV{PATH})) {
		my $f = $dir."/".$cmd;
		return $f if -e $f;
	}
	return undef;
}
sub run
{
	my @ARGS = @_;
	my $exe = which(shift @ARGS);
	return undef if ! defined $exe;
	#print STDERR join("<->", ($exe, @ARGS))."\n";
	exec($exe, @ARGS);
}
sub nc_direct
{
	my ($target_host, $target_port) = @_;
	# try socat first
	run('socat', 'STDIO', "TCP:$target_host:$target_port");
	# if it fails, try netcat
	run('nc', $target_host, $target_port);
}
sub nc_proxy
{
	my ($target_host, $target_port) = @_;

	# socat is more consistent than netcat, so try it first
	# SOCKS4 is not a typo, some folks found it more reliable
	# across socat versions than using SOCKS5
	run('socat', 'STDIO', "SOCKS4:${SOCKS5_SERVER}:$target_host:$target_port,socksport=$SOCKS5_PORT");

	# netcat-openbsd syntax (this is normal to find on Linux
	# systems and is default on Debian/Ubuntu).  Note: this
	# is known to be broken on F19.
	run('nc', '-X', '5', '-x', $SOCKS5_PROXY, $target_host, $target_port);
}

if ($host !~ /\./ || $host =~ /(^|\.)intel\.com$/ ||
		    $host =~ /^(10|172\.1[6789]|172\.2[0-9]|172\.3[01]|192\.168|192\.0\.2|143\.183|134\.134)\./) {
	    nc_direct($host, $port);
} else {
	    nc_proxy($host, $port);
}

