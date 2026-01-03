from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from hashlib import pbkdf2_hmac
from pathlib import Path
import os, json

with open("./config.json", "r") as r:
  config = json.load(r)

def encrypt(user, password):
  with open(f"/data/users/{user}.dat", "rb") as r:
    user = r.read()
  salt = os.urandom(config["security"]["salt"])
  nonce = os.urandom(config["security"]["nonce"])
  psw = bytearray(pbkdf2_hmac("sha256", password.encode("utf-8"), salt, config["security"]["iterations"], dklen=32))

  aes = AESGCM(psw)
  ciphertext = salt + nonce + aes.encrypt(nonce, Path(f"/data/users/{user}.dat"), None)
  with open(f"/data/users/{user}.dat", "wb") as w:
    w.write(ciphertext)

  psw[:] = b"\x00" * len(psw)
  del psw

def decrypt(user, password):
  with open(f"/data/users/{user}.dat", "rb") as r:
    user = r.read()
  salt = user[0:config["security"]["salt"]]
  nonce = user[config["security"]["salt"]:(config["security"]["salt"] + config["security"]["nonce"])]
  blob = user[28:]
  psw = bytearray(pbkdf2_hmac("sha256", password.encode("utf-8"), salt, config["security"]["iterations"], dklen=32))

  aes = AESGCM(psw)
  plaintext = aes.decrypt(nonce, blob, None).decode("utf-8")
  with open(f"/data/users/{user}.dat", "w") as w:
    json.dump(plaintext, w, indent=4)

  psw[:] = b"\x00" * len(psw)
  del psw
