from hashlib import sha256
import json, time, os

with open("./config.json", "r") as r:
  config = json.load(r)

def propagate():
  if not os.path.exists("/data/index.json"):
    timestamp = round(time.time())
    difficulty = config["blockchain"]["difficulty"].to_bytes((config["blockchain"]["difficulty"].bit_length() + 7) // 8, "big")

    static = (config["metadata"]["version"].to_bytes((config["metadata"]["version"].bit_length() + 7) // 8, "big") + ("0"*64).encode("utf-8") + (0).to_bytes(((0).bit_length() + 7) // 8, "big") + ("0"*64).encode("utf-8") + timestamp.to_bytes((timestamp.bit_length() + 7) // 8, "big") + difficulty + (0).to_bytes(((0).bit_length() + 7) // 8, "big") + (0).to_bytes(((0).bit_length() + 7) // 8, "big") + (0).to_bytes(((0).bit_length() + 7) // 8, "big"))
    hash = sha256(sha256(static).digest()).hexdigest()
    block =
    {
      "header": {
        "version": config["metadata"]["version"],
        "prevHash": "0"*64,
        "height": 0,
        "merkleRoot": "0"*64,
        "timestamp": timestamp,
        "difficulty": difficulty.hex(),
        "nonce": 0,
        "extraNonce": 0,
        "blockHash": hash
      },
      "body": []
    }
    with open("/data/index.json", "w") as w:
      temp = []
      temp.append(block)
      json.dump(temp, w, indent=4)
  else:
    with open("/data/index.json", "r") as r:
      index = json.load(r)
    latest = index[-1]
    previous = index[-2]

    timestamp = round(time.time())
    difficulty = round(int(latest["header"]["difficulty"], 16) * ((latest["header"]["timestamp"] - previous["header"]["timestamp"]) / 60))
    difficulty = difficulty.to_bytes((difficulty.bit_length() + 7) // 8, "big")
    height = latest["header"]["height"] + 1
    prevHash = bytes.fromhex(latest["header"]["blockHash"])

    static = (config["metadata"]["version"].to_bytes((config["metadata"]["version"].bit_length() + 7) // 8, "big") + prevHash + height.to_bytes((height.bit_length() + 7) // 8, "big") + ("0"*64).encode("utf-8") + timestamp.to_bytes((timestamp.bit_length() + 7) // 8, "big") + difficulty + (0).to_bytes(((0).bit_length() + 7) // 8, "big") + (0).to_bytes(((0).bit_length() + 7) // 8, "big") + (0).to_bytes(((0).bit_length() + 7) // 8, "big"))
    hash = sha256(sha256(static).digest()).hexdigest()
    block =
    {
      "header": {
        "version": config["metadata"]["version"],
        "prevHash": prevHash.hex(),
        "height": height,
        "merkleRoot": "0"*64,
        "timestamp": timestamp,
        "difficulty": difficulty.hex(),
        "nonce": 0,
        "extraNonce": 0,
        "blockHash": hash
      },
      "body": []
    }
    index.append(block)
    with open("/data/index.json", "w") as w:
      json.dump(index, w, indent=4)
