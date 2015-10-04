#!/usr/bin/env python2.7
# -*- coding=UTF-8 -*-
# Created at Jan 12 11:39 by BlahGeek@Gmail.com

import subprocess
import os
from hashlib import sha512
from tempfile import gettempdir
from PIL import Image, ImageDraw, ImageFont
import argparse


splitLine = lambda s, n: [s[n*i:n*i+n] for i in xrange(len(s)/n)]

def fixpasswd(p):
    magic = [10, 7, 9, 17, 27, 35]
    ret = ''
    for i, c in enumerate(p):
        delta = magic[i] - (i+1) ** 2 if i < len(magic) else 0
        ret += chr(ord(c) + delta)
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

def buildImage(lines, size=(150, 250)):
    background = (252, 244, 220)
    foreground = (83, 104, 112)
    font = ImageFont.truetype('Inconsolata-Regular.ttf', 28)
    img = Image.new('RGB', size, background)
    draw = ImageDraw.Draw(img)

    height = 10
    for i, line in enumerate(lines):
        textsize = draw.textsize(line, font=font)
        draw.text(((size[0] - textsize[0]) / 2, height), line, fill=foreground, font=font)
        height += textsize[1]

    filename = os.path.join(gettempdir(), 'mypasswd.png')
    with open(filename, 'wb') as f:
        img.save(f)
    return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate my password.')
    parser.add_argument('-p', '--password', help='Master password')
    parser.add_argument('-f', '--float', action='store_true', help='Output using screenfloat instead of stdout')
    parser.add_argument('domain', nargs='+', help='Domain, multiple arguments will be concatenated')

    args = parser.parse_args()

    passwd = args.password
    if not passwd:
        from getpass import getpass
        passwd = getpass('Password:')
    domain = ' '.join(args.domain)

    passwd = fixpasswd(passwd)
    result = generate(passwd, domain)
    if not args.float:
        print '\n'.join(result)
    else:
        img = buildImage(result)
        subprocess.check_output(['open', '-a', '/Applications/ScreenFloat.app', img])

