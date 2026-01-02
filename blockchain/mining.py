from hashlib import sha256
import json, os, threading

with open("./config.json", "r") as r:
  config = json.load(r)
with open("/data/index.json", "r") as r:
  index = json.load(r)

def pow():
  latest = index[-1]

  version = latest["header"]["version"].to_bytes((latest["header"]["version"].bit_length() + 7) // 8, "big")
  prevHash = None
  if prevHash == "0"*64:
    prevHash = ("0"*64).encode("utf-8")
  else:
    prevHash = bytes.fromhex(latest["header"]["prevHash"])
  height = latest["header"]["height"].to_bytes((latest["header"]["height"].bit_length() + 7) // 8, "big")
  merkleRoot = bytes.fromhex(latest["header"]["merkleRoot"])
  timestamp = latest["header"]["timestamp"].to_bytes((latest["header"]["timestamp"].bit_length() + 7) // 8, "big")
  difficulty = bytes.fromhex(latest["header"]["difficulty"])
  nonce = latest["header"]["nonce"].to_bytes((latest["header"]["nonce"].bit_length() + 7) // 8, "big")
  extraNonce = latest["header"]["extraNonce"].to_bytes((latest["header"]["extraNonce"].bit_length() + 7) // 8, "big")
  blockHash = latest["header"]["blockHash"]

  while nonce <= (2**32) - 1:
    nonce += 1
    blockHash = sha256(sha256(version + prevHash + height + merkleRoot + timestamp + difficulty + nonce.to_bytes((nonce.bit_length() + 7) // 8, "big") + extraNonce).digest()).hexdigest()
    if int(blockHash, 16) <= int.from_bytes(difficulty, "big"):
      break
    if nonce == (2**32) - 1:
      break
  if nonce == (2**32) - 1:
    while True:
      extraNonce += 1
      blockHash = sha256(sha256(version + prevHash + height + merkleRoot + timestamp + difficulty + nonce.to_bytes((nonce.bit_length() + 7) // 8, "big") + extraNonce.to_bytes((extraNonce.bit_length() + 7) // 8, "big")).digest()).hexdigest()
      if int(blockHash, 16) <= int.from_bytes(difficulty, "big"):
        break

  latest["header"]["nonce"] = nonce
  latest["header"]["extraNonce"] = extraNonce
  with open("/data/index.json", "w") as w:
    json.dump(latest, w, indent=4)

def start():
  cpuUsage = 0
  if config["blockchain"]["cpuUsage"] > 5:
    cpuUsage = 3
  else:
    cpuUsage = config["blockchain"]["cpuUsage"]
  usage = max(1, int(os.cpu_count() * (cpuUsage / 5)))

  threads = []
  for _ in range(usage):
    cpu = threading.Thread(target=pow)
    cpu.daemon = True
    cpu.start()
    threads.append(cpu)
  for thread in threads:
    thread.join()
    
