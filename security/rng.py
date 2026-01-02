import secrets, random, json
from hashlib import sha256

with open("./config.json", "r") as r:
  config = json.load(r)

def rand(start, stop):
  if config["rng"]["decision"] == "random":
    return random.randint(start, stop)
  elif config["rng"]["decision"] == "entropy":
    return secrets.randrange(start, stop + 1)
  else:
    return "233"
