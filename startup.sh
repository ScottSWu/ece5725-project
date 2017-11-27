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

# Start snowboy
./snowboy.py sb-sr.fifo &

# Start speech recognition
./speech-recognition.py sb-sr.fifo sr-ac.fifo &

# Start actuation
./actuation.py sr-ac.fifo &
