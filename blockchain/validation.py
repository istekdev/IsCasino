from hashlib import sha256
import json, os

with open("./config.json", "r") as r:
  config = json.load(r)

def start():
  with open("/data/index.json", "r") as r:
    index = json.load(r)

  difficulty = False

  for contents in index[-1]:
    if int(contents["header"]["blockHash"], 16) <= int(contents["header"]["difficulty"], 16):
      difficulty = True

  if difficulty == False:
    index.pop()
    with open("/data/index.json", "w") as w:
      json.dump(index, w, indent=4)
