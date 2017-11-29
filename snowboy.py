#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script performs hotword detection using Snowboy.
"""

import snowboy.snowboydecoder as sd
import sys

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: {} <model.pmdl>".format(sys.argv[0]))
    sys.exit(0)

  model = sys.argv[1]

  def write_detected():
    sys.stdout.write("HOTWORD\n")
    sys.stdout.flush()

  def interrupt_callback():
    return False

  detector = sd.HotwordDetector(model, sensitivity=0.5)

  # Main loop
  sys.stderr.write("Listening for hotword...\n")
  detector.start(detected_callback=write_detected,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

  detector.terminate()
