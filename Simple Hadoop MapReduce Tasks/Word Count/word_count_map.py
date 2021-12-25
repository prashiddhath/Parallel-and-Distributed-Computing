#!/usr/bin/env python

import sys

for line in sys.stdin:
  word_list = line.split()

  for word in word_list:
    print("%s\t%d" % (word, 1))