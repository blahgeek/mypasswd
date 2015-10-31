#!/usr/bin/env python2.7
# -*- coding=UTF-8 -*-
# Created at Jan 12 11:39 by BlahGeek@Gmail.com

from hashlib import sha512
import argparse


splitLine = lambda s, n: [s[n*i:n*i+n] for i in xrange(len(s)/n)]

def fixpasswd(p):
    magic = [10, 7, 9, 17, 27, 35]
    ret = ''
    for i, c in enumerate(p):
        delta = magic[i] - (i+1) ** 2 if i < len(magic) else 0
        ret += chr(ord(c) + delta)
    return ret

def extract(s):
    ret = ''

    p = -1
    for i, c in enumerate(s):
        if not c.isalpha():
            p = i
            break
    assert p != -1

    while True:
        p += 10
        if p >= len(s):
            break
        ret += s[p]

    p -= 10
    p = p+1 if p+1 < len(s) else p-9
    while len(ret) < 10:
        ret += s[p]
        p -= 10

    return ret

def hexToAscii(s):
    b = bin(int(s, 16)).partition('b')[2]
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
    parser = argparse.ArgumentParser(description='Generate my password.')
    parser.add_argument('-p', '--password', help='Master password')
    parser.add_argument('domain', nargs='+', help='Domain, multiple arguments will be concatenated')

    args = parser.parse_args()

    passwd = args.password
    if not passwd:
        from getpass import getpass
        passwd = getpass('Password:')
    domain = ' '.join(args.domain)

    passwd = fixpasswd(passwd)
    result = generate(passwd, domain)
    print extract(''.join(result))

