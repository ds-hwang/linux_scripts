#!/usr/bin/env python

"""
Proxy command script for at least SSH and Git.

It runs socat at the end. Requires python-ipaddr and socat. Everything else
should be part of standard python distribution.

Usage for SSH:
    ProxyCommand $HOME/bin/proxy_command.py %h %p

Usage for GIT:
    export GIT_PROXY_COMMAND=$HOME/bin/proxy_command.py
"""

import sys
import logging
import socket
import errno
import random
import os
import urllib2

import ipaddr

__author__ = "Andy Shevchenko <andriy.shevchenko@intel.com>"

HTTP_PROXY = "http://proxy-jf.intel.com:911"
SOCKS_PROXY = "http://proxy-jf.intel.com:1080"

LOG = logging.getLogger(sys.argv[0])

def get_proxy(xvar, defval):
    """Get proxy server address and port."""
    xproxy = urllib2.urlparse.urlparse(os.environ.get(xvar, defval))
    if xproxy.scheme:
        return xproxy.netloc.split(':')
    return xproxy.path.split(':')

def resolve(addr, port):
    """Resolve given address and port for TCP connection."""
    try:
        ais = socket.getaddrinfo(addr, port)
    except socket.gaierror, err:
        raise ValueError, "%s:%s: %s" % (addr, port, str(err))

    random.shuffle(ais)

    return [a[4][0] for a in ais if a[2] == socket.IPPROTO_TCP]

def get_addr(addr, port):
    """Make ipaddr object from given address and port."""
    return ipaddr.IPAddress(resolve(addr, port)[0])

def resolve_private(addr, port):
    """Resolve given private address and port for TCP connection."""
    return [a for a in resolve(addr, port) if ipaddr.IPAddress(a).is_private]

def get_private_addr(addr, port):
    """
        Make an ipaddr object from given address and port. Return None
        if no address found.
    """
    addresses = resolve_private(addr, port)
    if addresses:
        return ipaddr.IPAddress(addresses[0])
    return None

def main(args):
    """MAIN routine."""
    # Setup logging
    conh = logging.StreamHandler()
    LOG.addHandler(conh)
    #LOG.setLevel(logging.DEBUG)

    # Get CLI parameters
    if len(args) < 3:
        LOG.error("Invalid parameters")
        sys.exit(errno.EINVAL)

    addr = args[1]
    port = args[2]

    # Check address
    try:
        ipobj = get_private_addr(addr, port)
        if ipobj is None:
            ipobj = get_addr(addr, port)
    except ValueError, err:
        LOG.error(str(err))
        sys.exit(errno.EADDRNOTAVAIL)

    # Get SOCKS proxy address and port
    socks_proxy_obj = get_proxy("socks_proxy", SOCKS_PROXY)
    try:
        socks_proxy_addr = get_addr(socks_proxy_obj[0], socks_proxy_obj[1])
    except ValueError:
        socks_proxy_addr = None

    # Construct socat argument string
    if socks_proxy_addr is None or ipobj.is_private or ipobj.is_loopback:
        socat_arg = "TCP:%s:%s" % (addr, port)
    else:
        socat_arg = "SOCKS:%s:%s:%s,socksport=%s" % \
            (socks_proxy_obj[0], addr, port, socks_proxy_obj[1])

    LOG.debug("socat parameters: %s", socat_arg)

    os.execlp("socat", args[0], "STDIO", socat_arg)

if __name__ == '__main__':
    main(sys.argv)

