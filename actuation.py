#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script actuates the servo to press buttons accordingly
"""

from servo import Servo
import sys
import time

BUTTON_PIN = 13 # PWM1

if __name__ == "__main__":
  if len(sys.argv) < 1:
    print("Usage: python {}".format(sys.argv[0]))
    sys.exit(0)

  button = Servo(BUTTON_PIN)
  button.start()
  line = ""
  while line != "QUIT":
    line = sys.stdin.readline().strip()
    if line == "0": # cancel
      if last_time - time.time() < 30:
        if last_action == 1:
          button.set_speed(0.20)
          time.sleep(1)
          button.set_speed(0)
        elif last_action == 2:
          button.set_speed(-0.32)
          time.sleep(1)
          button.set_speed(0)
        last_action = 0
    elif line == "1": # espresso
      button.set_speed(0.20)
      time.sleep(1)
      button.set_speed(0)
      last_action = 1
      last_time = time.time()
    elif line == "2": # large
      button.set_speed(-0.32)
      time.sleep(1)
      button.set_speed(0)
      last_action = 2
      last_time = time.time()
    # TODO Capsule cover commands

  f.close()
