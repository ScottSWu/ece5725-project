#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script trains the phrases in the "phrases" folder.
"""

import numpy
import os
from sklearn import linear_model
from sklearn.externals import joblib
import sys

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: python {} <training data...> <output model>".format(sys.argv[0]))
    sys.exit(0)

  inputs = sys.argv[1:-1]
  names = [os.path.basename(os.path.dirname(i)) for i in inputs]
  output = sys.argv[-1]

  x = []
  y = []
  for i, input in enumerate(inputs):
    train = numpy.load(input)
    x.extend(train)
    y.extend([i] * len(train))

  lreg = linear_model.LogisticRegression(C=1e5)
  lreg.fit(x, y)
  joblib.dump(lreg, output)
