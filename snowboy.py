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
    print("Usage: {} <sb-sr.fifo> <model.pmdl>".format(sys.argv[0]))
    sys.exit(0)

  fout = [open(sys.argv[1], 'r')]
  model = sys.argv[2]

  def write_detected():
    fout[0].write("HOTWORD\n")

  def interrupt_callback():
    print("Interrupt")
    sys.exit(0)

  detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

  # Main loop
  print("Listening for hotword...")
  detector.start(detected_callback=write_detected,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)

  detector.terminate()
