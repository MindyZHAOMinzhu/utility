#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Extract abstract from a tex source which is good enough to be
# pasted into the submission system.
#
# Test: python -m doctest tex-extract-abstract.py -v

"""
Usage:
    tex-extract-abstract.py <tex_file>
    tex-extract-abstract.py (-h | --help)

Options:
    -h --help     Show this screen.
"""


import sys
import re

def extract_abstract(source):
    '''
    :param source:
        The TeX source string

    >>> extract_abstract('\\\\begin{abstract}\\nabstract here\\n\\\\end{abstract}')
    u'abstract here'
    >>> extract_abstract('\\\\begin{abstract}\\nabstract here\\nand here\\n\\\\end{abstract}')
    u'abstract here and here'
    >>> extract_abstract('\\\\begin{abstract}\\nabstract here.\\n  %commented line\\nand here\\n\\\\end{abstract}')
    u'abstract here. and here'
    >>> extract_abstract('\\\\begin{abstract}\\nabstract here %commented.\\n  %commented line\\nand here\\n\\\\end{abstract}')
    u'abstract here and here'
    '''
    if isinstance(source, str):
        source = source.decode('utf-8')
    abstract = []
    in_abstract = False
    for line in source.split('\n'):
        line = line.strip()
        if line.startswith(r'\begin{abstract}'):
            in_abstract = True
            continue
        if line.startswith(r'\end{abstract}'):
            in_abstract = False
            break
        if in_abstract:
            line = re.sub(r'%.*$', r'', line).strip()
            #print 'line "%s"' % line
            if line:
                abstract.append(line)
    return ' '.join(abstract)


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__, version='tex-extract-abstract.py 0.1')
    tex_file = arguments['<tex_file>']
    if tex_file is None:
        # Input from stdin
        source = sys.stdin.read()
    else:
        source = open(tex_file, 'r').read()
    print extract_abstract(source)
