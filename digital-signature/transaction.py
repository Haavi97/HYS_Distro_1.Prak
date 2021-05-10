from digital_signature import DigitalSignature
from datetime import datetime
import binascii
import json

class TransAction:
  def __init__(self):
    self.digital_signature = DigitalSignature()
    self.userpath = '../server-client/users'
  
  def create_transaction(self, user_from, user_to, sum):

    public_from = self.digital_signature.get_public_key(user_from)
    public_to = self.digital_signature.get_public_key(user_from)
    transaction = {
      "from":  binascii.hexlify(self.digital_signature.key_to_string(public_from)).decode(),
      "to":  binascii.hexlify(self.digital_signature.key_to_string(public_to)).decode(),
      "sum": sum,
      "timestamp": datetime.now().isoformat()
    }
    final = {
      "signature": binascii.hexlify(self.digital_signature.create_signature(bytes(str(transaction), 'utf-8'), user_from)).decode(),
      "transaction": transaction
    }
    return json.dumps(final)
  
if __name__ == '__main__':
  trans = TransAction()
  print(trans.create_transaction('user1', 'user2', 0.05))

