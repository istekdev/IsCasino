from bip_utils import Bip32Slip10Secp256k1
from Crypto.Hash import RIPEMD
from mnemonic import Mnemonic
import os, base58, json, time
from hashlib import sha256

with open("./config.json", "r") as r:
  config = json.load(r)

MN = Mnemonic("english")

def pseudoGen():
  with open("/data/usernames.json", "r") as r:
    names = json.load(r)
  seed = MN.to_seed(MN.to_mnemonic(os.urandom(config["security"]["mnemonic"])), passphrase="")
  bip = Bip32Slip10Secp256k1.FromSeed(seed)

  core = bip.DerivePath(config["security"]["path"])
  private = core.PrivateKey().Raw().ToBytes()
  public = core.PublicKey().RawCompressed().ToBytes()

  pseudos =
  {
    "user": names.pop(),
    "privateKey": private.hex(),
    "publicKey": public.hex()
  }
  return pseudos
  

def generate(user):
  global seedPhrase, username
  for identicals in os.listdir("/data/users/"):
    if user in identicals:
      username = f"{user}_{(os.urandom(10)).hex()}"
    else:
      username = user
  id = os.urandom(20)
  timestamp = round(time.time())
  network = "IsCasino-main"
  tampered = False
  
  entropy = bytearray(os.urandom(config["security"]["mnemonic"]))
  seedPhrase = MN.to_mnemonic(entropy)
  seed = bytearray(MN.to_seed(seedPhrase, passphrase=""))
  bip = Bip32Slip10Secp256k1.FromSeed(seed)

  core = bip.DerivePath(config["security"]["path"])
  private = bytearray(core.PrivateKey().Raw().ToBytes())
  public = core.PublicKey().RawCompressed().ToBytes()

  static = (network.encode("utf-8") + username.encode("utf-8") + id + timestamp.to_bytes((timestamp.bit_length() + 7) // 8, "big") + config["security"]["path"].encode("utf-8") + private + public + str(tampered).encode("utf-8"))
  verifyHash = sha256(static).hexdigest()

  metadata =
  {
    "metadata": {
      "network": network,
      "user": username,
      "id": id.hex(),
      "timestamp": timestamp
    },
    "security": {
      "path": config["security"]["path"],
      "privateKey": private.hex(),
      "publicKey": public.hex(),
      "tampered": tampered,
      "verifyHash": verifyHash
    }
  }
  with open(f"/data/users/{username}.dat", "w") as w:
    json.dump(metadata, w, indent=4)

  entropy[:] = b"\x00" * len(entropy)
  seed[:] = b"\x00" * len(seed)
  private[:] = b"\x00" * len(private)
  del entropy, seed, private
