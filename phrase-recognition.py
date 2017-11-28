#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script performs phrase recognition using a pre-trained model.
"""

import pyaudio
import sys
from sklearn.externals import joblib

SAMPLE_RATE = 44100
CHECK_FRAMES = 1024

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
      # Listen for at most 3 seconds
      frames = []
      chunks = 0
      last = 0
      chunks_per_second = float(SAMPLE_RATE) / float(CHECK_FRAMES)
      while chunks < chunks_per_second * 3 or (len(frames) > 0 and chunks - last > chunks_per_second):
        data = stream.read(CHUNK)
        if isActive(data):
          frames.extend(data)
          last = chunks

        chunks += 1

      if len(frames) / chunks_per_second > 0.5:
        normalized = processFrequency(frames)
        z = lreg.predict([normalized])
        print("Detected", z)
        fac.write("{}\n".format(z[0]))

  fsb.close()
  fac.close()
