#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script performs phrase recognition using a pre-trained model.
"""

import math
import numpy as np
from numpy.fft import fft
import pyaudio
import sys
from sklearn.externals import joblib

SAMPLE_RATE = 44100
SAMPLE_FREQ = 44100
CHECK_FRAMES = 1024

AMPLITUDE_THRESHOLD = 0.01
THRESHOLD_FRACTION = 0.1
SAMPLE_WIDTH = 2
ACTIVITY_THRESHOLD = AMPLITUDE_THRESHOLD * math.pow(2, SAMPLE_WIDTH * 8 - 1)
THRESHOLD_FRAMES = int(THRESHOLD_FRACTION * CHECK_FRAMES)

VOICE_MIN = 100
VOICE_MAX = 3000
FREQUENCY_MIN = int(math.floor(VOICE_MIN / (float(SAMPLE_FREQ) / CHECK_FRAMES)))
FREQUENCY_MAX = int(math.ceil(VOICE_MAX / (float(SAMPLE_FREQ) / CHECK_FRAMES)))

BIT_WIDTH = 1 << (SAMPLE_WIDTH * 8)
HALF_BIT_WIDTH = BIT_WIDTH / 2

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
  size = float(len(freqs))
  if size < 1.0:
    raise Exception("Not enough data!")

  avg = freqs[0]
  for f in freqs:
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

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("Usage: python {} <model.pkl> <sb-sr.fifo> <sr-ac.fifo>".format(sys.argv[0]))
    sys.exit(0)

  lreg = joblib.load(sys.argv[1])
  fsb = open(sys.argv[2], 'r')
  fac = open(sys.argv[3], 'w')

  p = pyaudio.PyAudio()
  stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHECK_FRAMES)

  line = ""
  while line != "QUIT":
    line = fsb.readline().strip()
    if line == "HOTWORD":
      print("Listening for phrase...")

      # Listen for at most 3 seconds
      frames = []
      chunks = 0
      last = 0
      chunks_per_second = float(SAMPLE_RATE) / float(CHECK_FRAMES)

      while chunks < chunks_per_second * 3 and (len(frames) == 0 or chunks - last < chunks_per_second):
        data = convert(stream.read(CHECK_FRAMES))
        if isActive(data):
          frames.extend(data)
          last = chunks

        chunks += 1

      print("End listning for phrase")
      if len(frames) / chunks_per_second > 0.5:
        normalized = processFrequency(frames)
        z = lreg.predict([normalized])
        print("Detected", z)
        fac.write("{}\n".format(z[0]))
        fac.flush()

  fsb.close()
  fac.close()
