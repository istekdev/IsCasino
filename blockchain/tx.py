from Crypto.Hash import RIPEMD160
import time, json, ecdsa, base58
from hashlib import sha256

with open("./config.json", "r") as r:
  config = json.load(r)
with open("/data/index.json", "r") as r:
  index = json.load(r)

def verify(tx, signing, publicKey):
  sign = bytearray(signing)
  
  sender = False
  receiver = False
  nonce = False
  amount = False
  signature = False
  txid = False
  
  transaction = json.dumps(tx, indent=4)
  send = base58.b58decode(transaction["from"][2:])
  receive = base58.b58decode(transaction["to"][2:])

  if sha256(sha256(send[0:1] + send[1:21]).digest()).digest()[:4] == send[21:25]:
    sender = True
  if sha256(sha256(receive[0:1] + receive[1:21]).digest()).digest()[:4] == receive[21:25]:
    receiver = True
  verNonce = 0
  for txs in index:
    if txs.get("body"):
      verNonce += len(txs["body"])
      verNonce = verNonce + 1
  if transaction["nonce"] == verNonce:
    nonce = True
  tos = 0
  froms = 0
  for txs in index:
    for tx in txs.get("body", []):
      if tx.get("to") == transaction["from"]:
        tos += tx.get("amount", 0)
  for txs in index:
    for tx in txs.get("body", []):
      if tx.get("from") == transaction["from"]:
        froms += tx.get("amount", 0)
  if (tos - froms) < transaction["amount"]:
    amount = False
  sigStatic = (transaction["to"].encode("utf-8") + transaction["from"].encode("utf-8") + transaction["amount"].to_bytes((transaction["amount"].bit_length() + 7) // 8, "big") + transaction["timestamp"].to_bytes((transaction["timestamp"].bit_length() + 7) // 8, "big") + transaction["nonce"].to_bytes((transaction["nonce"].bit_length() + 7) // 8, "big"))
  static = (transaction["to"].encode("utf-8") + transaction["from"].encode("utf-8") + transaction["amount"].to_bytes((transaction["amount"].bit_length() + 7) // 8, "big") + transaction["timestamp"].to_bytes((transaction["timestamp"].bit_length() + 7) // 8, "big") + transaction["nonce"].to_bytes((transaction["nonce"].bit_length() + 7) // 8, "big") + bytes.fromhex(transaction["signature"]))
  if sign.sign_digest(sha256(sigStatic).digest()) == bytes.fromhex(transaction["signature"]):
    signature = True
  if sha256(static).hexdigest() == transaction["txid"]:
    txid = True

  if sender and receiver and nonce and amount and signature and txid:
    return True
  else:
    return False

def construct(receiver, sender, amount, privateKey, publicKey):
  global status
  status = False
  signing = bytearray(ecdsa.SigningKey.from_string(bytes.fromhex(privateKey), curve=SECP256k1))
  
  timestamp = round(time.time())
  nonce = 0
  for txs in index:
    if txs.get("body"):
      nonce += len(txs["body"])
      nonce = nonce + 1
  signature = signing.sign_digest(sha256(receiver.encode("utf-8") + sender.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big") + timestamp.to_bytes((timestamp.bit_length() + 7) // 8, "big") + nonce.to_bytes((nonce.bit_length() + 7) // 8, "big")).digest())
  static = (receiver.encode("utf-8") + sender.encode("utf-8") + amount.to_bytes((amount.bit_length() + 7) // 8, "big") + timestamp.to_bytes((timestamp.bit_length() + 7) // 8, "big") + nonce.to_bytes((nonce.bit_length() + 7) // 8, "big") + signature)
  txid = sha256(static).hexdigest()
  tx =
  {
    "to": receiver,
    "from": sender,
    "amount": amount,
    "timestamp": timestamp,
    "nonce": nonce,
    "signature": signature.hex(),
    "txid": txid
  }
  if verify(tx, signing, publicKey):
    index[-1]["body"].append(tx)
    with open("/data/index.json", "w") as w:
      json.dump(index, w, indent=4)
    status = True
  else:
    pass
    
  signing[:] = b"\x00" * len(signing)
  del signing
