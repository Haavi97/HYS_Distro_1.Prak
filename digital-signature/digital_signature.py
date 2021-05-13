import os

from ecdsa import SigningKey, VerifyingKey, BadSignatureError

class DigitalSignature:
  def __init__(self):
    self.userpath = '..' + os.sep + 'server-client' + os.sep + 'users'

  def create_key(self, name):
    print(self.userpath + os.sep + name + os.sep + "sk.pem")
    sk = SigningKey.generate()
    vk = sk.verifying_key
    with open(self.userpath + os.sep + name + os.sep + "sk.pem", "wb") as f:
      f.write(sk.to_pem())
    with open(self.userpath + os.sep + name + os.sep + "vk.pem", "wb") as f:
      f.write(vk.to_pem())
    return sk.to_string(), vk.to_string()

  def get_public_key(self, name):
    with open(self.userpath + os.sep + name + os.sep + "vk.pem") as f:
      vk = VerifyingKey.from_pem(f.read())
    return vk

  def key_to_string(self, key):
    return key.to_string()
  
  def string_to_sk_key(self, sk_string):
    return SigningKey.from_string(sk_string)

  def string_to_vk_key(self, vk_string):
    return VerifyingKey.from_string(vk_string)

  def create_signature(self, message, name):
    with open(self.userpath + os.sep + name + os.sep + "sk.pem") as f:
      sk = SigningKey.from_pem(f.read())
      signature = sk.sign(message)
    return signature

  def verify_signature(self, vk, signature, message):
    try:
      return vk.verify(signature, message)
    except BadSignatureError:
        return False

if __name__ == '__main__':
  digi = DigitalSignature()
  digi.create_key('user1')
  print(digi.key_to_string(digi.get_public_key('user1')))
  message = b"message"
  signature = digi.create_signature(message, 'user1')
  print(digi.verify_signature(digi.get_public_key('user1'), signature, b"message"))
  
