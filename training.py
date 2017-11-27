#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script trains the phrases in the "phrases" folder.
"""

import sys

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python {} <output>".format(sys.argv[0]))
    sys.exit(0)
