#!/bin/bash

# Charles Bai (cb674)
# Scott Wu (ssw74)
# ECE 5725 Final Project

# Create the FIFO queue file
if [ ! -f sb-sr.fifo ]; then
  mkfifo sb-sr.fifo
fi
if [ ! -f sr-ac.fifo ]; then
  mkfifo sr-ac.fifo
fi

# Flush the queues
dd if=sb-sr.fifo iflag=nonblock of=/dev/null
dd if=sr-ac.fifo iflag=nonblock of=/dev/null

python snowboy.py snowboy/alexa.umdl | python phrase-recognition.py phrases/model.pkl | python actuation.py sr-ac.fifo

