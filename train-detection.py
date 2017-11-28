#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This test script detects training data in a wave file.
"""

import math
import wave
import sys
import glob
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft

def parse(win):
  # Check for "activity" every x samples, split into x time windows
  SAMPLE_FREQ = win.getframerate()
  CHECK_FRAMES = 1024
  TIME_BINS = 1
  HALF_SECOND = int(SAMPLE_FREQ * 0.5)

  # Arbitrarily pick a threshold
  AMPLITUDE_THRESHOLD = 0.01
  THRESHOLD_FRACTION = 0.1
  SAMPLE_WIDTH = win.getsampwidth()
  ACTIVITY_THRESHOLD = AMPLITUDE_THRESHOLD * math.pow(2, SAMPLE_WIDTH * 8 - 1)
  THRESHOLD_FRAMES = int(THRESHOLD_FRACTION * CHECK_FRAMES)

  # Only keep track of these voice frequencies
  VOICE_MIN = 100
  VOICE_MAX = 3000
  FREQUENCY_MIN = int(math.floor(VOICE_MIN / (float(SAMPLE_FREQ) / CHECK_FRAMES)))
  FREQUENCY_MAX = int(math.ceil(VOICE_MAX / (float(SAMPLE_FREQ) / CHECK_FRAMES)))

  # Width of sample value
  BIT_WIDTH = 1 << (SAMPLE_WIDTH * 8)
  HALF_BIT_WIDTH = BIT_WIDTH / 2

  # Other properties
  TOTAL_FRAMES = win.getnframes()

  print("Total frames: %d" % TOTAL_FRAMES)
  print("Check frame size: %d" % CHECK_FRAMES)
  print("Sampling frequency: %d" % SAMPLE_FREQ)
  print("Activity threshold: %f" % ACTIVITY_THRESHOLD)
  print("Frames threshold: %d" % THRESHOLD_FRAMES)
  print("Voice frequency: %d - %d" % (FREQUENCY_MIN, FREQUENCY_MAX))

  # Utility functions
  # Convert LE string to number
  def le(data):
    value = 0
    for i in range(len(data)):
      value += data[i] << (8 * i)

    if value >= HALF_BIT_WIDTH:
      value = value - BIT_WIDTH

    return value

  # Convert LE string to array
  def convert(chunk):
    return [le(chunk[i:i+SAMPLE_WIDTH]) for i in range(0, len(chunk), SAMPLE_WIDTH)]

  # Check if the section satisfies the activity threshold
  def isActive(data):
    count = 0
    for amplitude in data:
      if abs(amplitude) > ACTIVITY_THRESHOLD:
        count += 1

    return count > THRESHOLD_FRAMES

  def average(data):
      return float(sum(data)) / len(data)

  # Processing functions
  def processFrequency(data):
    count = len(data)

    if count < CHECK_FRAMES:
      raise Exception("Not enough data!")

    freqs = []
    for chunk in range(0, count - CHECK_FRAMES + 1, CHECK_FRAMES):
      # Take the fft in chunks
      magnitude = np.absolute(fft(data[chunk:(chunk + CHECK_FRAMES)]))[:(CHECK_FRAMES // 2)]
      freqs.append(magnitude)

    # Average and flatten in groups
    groups = []
    size = float(len(freqs)) // TIME_BINS
    if size < 1.0:
      raise Exception("Not enough data!")

    for chunk in range(0, TIME_BINS):
      start = int(chunk * size)
      end = int((chunk + 1) * size)
      avg = freqs[start]
      for f in freqs[start+1:end]:
          avg = [x + y for x, y in zip(avg, f)]

      # Only take relevant frequencies
      avg = avg[FREQUENCY_MIN:FREQUENCY_MAX]
      avg = [float(i) / size for i in avg]
      # Normalize by the mean
      mean = average([abs(i) for i in avg])
      normalized = [i / mean for i in avg]
      groups.append(normalized)

    flat = [i for sl in groups for i in sl]

    return flat

  def processAmplitude(data):
    NORMALIZED_SIZE = 200
    points = len(data)

    # Absolute value
    positive = [abs(i) for i in data]

    # Normalize by the mean
    avg = average(positive)
    normalized = [i / avg for i in data]

    # Resize down to 200 points
    interval = float(points) / NORMALIZED_SIZE

    resized = [average(normalized[int(i*interval):int((i+1)*interval)])
        for i in range(NORMALIZED_SIZE)]

    return resized

  # Rewind to the beginning
  win.rewind()

  # Number of frames read
  read = 0
  # Current state of reading (background, foreground)
  state = 0
  foreground = []
  background = []
  count = 0
  train = []
  while read < TOTAL_FRAMES:
    next = convert(win.readframes(CHECK_FRAMES))
    #print "\n".join([str(i) for i in next])
    active = isActive(next)

    if state == 0:
      if active:
        last = read
        foreground.extend(next)
        state = 1
        print("Begin: {}".format(float(last) / float(SAMPLE_FREQ)))
    elif state == 1:
      if active:
        last = read
        foreground.extend(next)
      else:
        state = 2
    elif state == 2:
      if active:
        state = 1
        last = read
        foreground.extend(background)
        foreground.extend(next)
        background = []
      elif read - last >= HALF_SECOND:
        state = 0
        print("End:   {}".format(float(last) / float(SAMPLE_FREQ)))
        foreground.extend(background)
        normalized = processFrequency(foreground)
        train.append(normalized)
        foreground = []
        background = []
      else:
        background.extend(next)

    read += CHECK_FRAMES

  return train

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: python {} <wave file> <output>".format(sys.argv[0]))
    sys.exit(0)

  win = wave.open(sys.argv[1], "rb")
  train = parse(win)

  fout = open(sys.argv[2], "wb")
  np.save(fout, train)

  for sample in train:
    plt.plot(sample)

  plt.show()
