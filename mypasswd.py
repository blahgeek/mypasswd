#!/usr/bin/env python2
# -*- coding=UTF-8 -*-
# Created at Jan 12 11:39 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')


import os
from hashlib import sha512
from getpass import getpass
from tempfile import gettempdir


splitLine = lambda s, n: [s[n*i:n*i+n] for i in xrange(len(s)/n)]

def hexToAscii(s):
    b = bin(int(s, 16)).partition('b')[2]
    print b
    chs = splitLine(b, 6)
    ret = [chr(int(ch, 2) + 63) for ch in chs]
    return ''.join(ret)

def generate(passwd, domain):
    passwd = passwd.strip()
    domain = domain.strip()
    for i in xrange(10):
        passwd = sha512(passwd).hexdigest()
    ret = passwd + domain
    for i in xrange(10):
        ret = sha512(ret).hexdigest()
    ret = hexToAscii(ret)
    return splitLine(ret, 10)

if __name__ == '__main__':
    if sys.argv[1] == '--gui':
        import subprocess
        passwd = subprocess.check_output(
                ['zenity', '--password', '--title=My Password'])
        domain = subprocess.check_output(
                ['zenity', '--entry', '--title=My Password', '--text=Domain:'])
    else:
        passwd = getpass('Password: ')
        domain = ' '.join(sys.argv[1:])
    ret = '\n'.join(generate(passwd, domain))
    if sys.argv[1] == '--gui':
        fname = os.path.join(gettempdir(), 'my_passwd')
        with open(fname, 'w') as f:
            f.write(ret)
        try:
            subprocess.check_output(
                    ['zenity', '--width=50', '--height=330', '--text-info', \
                     '--filename='+fname, '--font=Monospace 18', '--title=My Password'])
        except subprocess.CalledProcessError:
            pass
        os.remove(fname)
    else:
        print ret
