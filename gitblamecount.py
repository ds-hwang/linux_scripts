#!/usr/bin/env python3
import sys
import os
import subprocess
import re
import collections
import pprint

count = collections.Counter()
p = re.compile(r'.+ \(([\w\W]+) [0-9]{4}-[0-9]{2}-[0-9]{2}.*', re.UNICODE)

path=sys.argv[1]
git_path=path
os.chdir(git_path)
for file in os.listdir(os.getcwd()):
        blame = subprocess.check_output(["git", "blame", "-w", "--abbrev=10", file],
                        stderr=subprocess.STDOUT)
        for line in blame.splitlines():
                m = p.match(str(line, 'utf-8'))
                name = str(m.group(1))
                name = name.rstrip()
                count[name] += 1

print("total lines counted: " + str(sum(count.values())) + " (compare with git ls-files -- " + git_path + " | xargs wc -l)")
pprint.pprint(count.most_common(10))
