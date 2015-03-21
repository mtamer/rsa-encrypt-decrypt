# Inorder to run this program, you have to run: python decrypt.py file_1.txt file_2.txt file_3.txt public_key_alice.pem private_key_bob.pem
import sys
import random
import Crypto.Util.number
import math
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from Crypto import Random
import base64
from Crypto.Signature import PKCS1_v1_5



with open(sys.argv[1]) as f:
    file_1 = f.read()
with open(sys.argv[2]) as f:
    file_2 = f.read()
with open(sys.argv[3]) as f:
    file_3 = f.read()
with open(sys.argv[4]) as f:
    public_key_a = f.readlines()[0] 
with open(sys.argv[5]) as f:
    private_key_b = f.readlines()[0] 
  


def decrypt_RSA(private_key_loc, package):
    from Crypto.PublicKey import RSA 
    from Crypto.Cipher import PKCS1_OAEP 
    from base64 import b64decode 
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    decrypted = rsakey.decrypt(b64decode(package)) 
    return decrypted

symmetric_key = decrypt_RSA( sys.argv[5], file_1)
print "After decrpypting file 1 we recieved the symmetric key: "+symmetric_key+ "\n"

def decrypt(ciphertext):
    # initialization vector from the ciphertext (the first part)
    iv = ciphertext[:AES.block_size]
    # get a cipher object to encrypt/decrypt with
    cipher = AES.new(symmetric_key, AES.MODE_CBC, iv)
    # decrypt the ciphertext
    plaintext = cipher.decrypt(ciphertext[AES.block_size:]) 
    # take out the padded characters to get the original string
    #print plaintext.rstrip(b"\0")
    return plaintext.rstrip(b"\0") 

message = decrypt(file_3)
print "The following message is returned when decrypting file_3 with the symmetric key: "+ message +"\n"

# Verify the signature
key = RSA.importKey(open(sys.argv[4]).read())
h = SHA256.new(message)
verifier = PKCS1_v1_5.new(key)
if verifier.verify(h, file_2):
   print "The signature is authentic."
else:
   print "The signature is not authentic."