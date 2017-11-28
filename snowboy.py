#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script performs hotword detection using Snowboy.
"""

import snowboydecoder
import sys

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: {} <model.pmdl>".format(sys.argv[0]))
    sys.exit(0)

  model = sys.argv[1]

  detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

  # Main loop
  print("Listening...")
  detector.start(detected_callback=snowboydecoder.play_audio_file,
                interrupt_check=.interrupt_callback,
                sleep_time=0.03)

  detector.terminate()
