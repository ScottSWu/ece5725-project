#!/usr/bin/python

"""
Charles Bai (cb674)
Scott Wu (ssw74)
ECE 5725 Final Project

This script submits wave files for training on snowboy.
"""

import base64
import requests
import sys

def get_wave(fname):
  with open(fname, "rb") as infile:
    return base64.b64encode(infile.read()).decode("utf8")


endpoint = "https://snowboy.kitt.ai/api/v1/train/"

############# MODIFY THE FOLLOWING #############
token = "5a1a6f958507a32f68ebcf25df8da8cb21f23d3a"
hotword_name = "Aron"
language = "en"
age_group = "20_29"
gender = "M"
microphone = "USB microphone"
############### END OF MODIFY ##################

if __name__ == "__main__":
  try:
    [_, wav1, wav2, wav3, out] = sys.argv
  except ValueError:
    print("Usage: %s wave_file1 wave_file2 wave_file3 out_model_name" % sys.argv[0])
    sys.exit()

  data = {
    "name": hotword_name,
    "language": language,
    "age_group": age_group,
    "gender": gender,
    "microphone": microphone,
    "token": token,
    "voice_samples": [
      {"wave": get_wave(wav1)},
      {"wave": get_wave(wav2)},
      {"wave": get_wave(wav3)}
    ]
  }

  response = requests.post(endpoint, json=data)
  if response.ok:
    with open(out, "wb") as outfile:
      outfile.write(response.content)
    print("Saved model to '%s'." % out)
  else:
    print("Request failed.")
    print(response.text)
