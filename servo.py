#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project
"""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Servo():
  def __init__(self, pin):
    GPIO.setup(pin, GPIO.OUT)
    self.pin = pin
    self.pwm = GPIO.PWM(pin, 50)
    self.stopped = True
    self.last_dc = 0
    self.set_speed(0)

  def start(self):
    self.pwm.start(self.last_dc)
    self.stopped = False

  # -1 to 1
  def set_speed(self, speed):
    if not self.stopped:
      dc = (speed * 0.2 + 1.5) / 20.0 * 100.0
      self.pwm.ChangeDutyCycle(dc)
      self.last_dc = dc

  def stop(self):
    self.pwm.ChangeDutyCycle(0)
    self.stopped = True
