#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script performs phrase speech recognition using phrase.pkl.
"""

import sys

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: python {} sb-sr.fifo sr-ac.fifo".format(sys.argv[0]))
    sys.exit(0)

  fsb = open(sys.argv[1], 'r')
  fac = open(sys.argv[2], 'w')
  line = ""
  while line != "QUIT":
    line = fsb.readline().strip()
    if line == "HOTWORD":
      # TODO start phrase detection
      fac.write("\n")

  fsb.close()
  fac.close()
