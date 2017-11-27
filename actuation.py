#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project
"""

from servo import Servo
import sys
import time

BUTTON_PIN = 3
CAPSULE_PIN = 4

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python {} sr-ac.fifo".format(sys.argv[0]))
    sys.exit(0)

  button = Servo(BUTTON_PIN)
  capsule = Servo(CAPSULE_PIN)
  f = open(sys.argv[1], 'r')
  line = ""
  while line != "QUIT":
    line = f.readline().strip()
    if line == "BUTTON1":
      button.set_speed(-1)
      time.sleep(1000)
      button.set_speed(0)
    elif line == "BUTTON2":
      button.set_speed(1)
      time.sleep(1000)
      button.set_speed(0)
    # TODO Capsule cover commands

  f.close()
