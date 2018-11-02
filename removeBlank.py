#! /usr/bin/env python
 
from tempfile import mkstemp
from shutil import move
from os import remove
import sys
import re
 
def replace(source_file_path):
    fh, target_file_path = mkstemp()
    blank_re = re.compile(r'\s+$')
    content_blank_re = re.compile(r'(.*)\s+$')
    changed = False;
    with open(target_file_path, 'w') as target_file:
        with open(source_file_path, 'r') as source_file:
            for line in source_file:
                m = blank_re.match(line)
                m2 = content_blank_re.match(line)
                if m:
                    target_file.write("\n")
                    changed = True;
                elif m2: 
                    newline = line.rstrip()
                    target_file.write(newline + "\n")
                    changed = True;
                else:
                    target_file.write(line)

    if changed:
        remove(source_file_path)
        move(target_file_path, source_file_path)
        print "file changed:%s" % (source_file_path) 
 
 
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for file in sys.argv[1:len(sys.argv)]:
            replace(file)
    else:
        print """Invalid command
        Usage: removeBlank.py [source_file_path]+
        """
