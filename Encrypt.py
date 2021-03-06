# In order to run this program, you have to run: python encrypt.py secret.txt public_key_bob.pem private_key_alice.pem
import sys
import random
import Crypto.Util.number
import math
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


# The following is the symmetric key generated by Alice that she uses to 
# encrypt the message file and and encrypts the key itself with bob's
# public key
# the key to encrypt decrypt symmetrically with
symmetricKey = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'

# This open function opens the first file which is message that Alice wants
# to send to Bob and reads the message
with open(sys.argv[1]) as f:
    message = f.readlines()[0]

# Prints the message to be encrypted
print "The message to be encrypted is : " + message+ "\n"
# Prints the symmetric key used to encrypt the message
print "The symmetric key used to encrypt the above message is: "+ symmetricKey

# This function encrypts a message using the RSA public key 
# with PKCS1-OAEP padding
def encryptKey(public_key_file, message):
    key = open(public_key_file, "r").read()
    rsa_key = RSA.importKey(key)
    rsa_key = PKCS1_OAEP.new(rsa_key)
    encryptedMessage = rsa_key.encrypt(message)
    return encryptedMessage.encode('base64')
# Write the encrypted message into file_1.txt   
file_1 = encryptKey(sys.argv[2], symmetricKey)
f1 = open('file_1.txt','w')
f1.write(file_1)
f1.close()
print "file_1.txt consists of the symmetric key encrypted with the public key"

# The following command takes in our third argument which is the private key.
private_key = RSA.importKey(open(sys.argv[3]).read())
# We then sign the data using the private key with PKCS1 v1.5 padding and
# SHA256 hash
hashed_message = SHA256.new(message)
signer = PKCS1_v1_5.new(private_key)
sign = signer.sign(hashed_message)

# Write the signed hash into file_2.txt
file_2 = sign
f2 = open('file_2.txt','w')
f2.write(file_2)
f2.close()
print "file_2.txt is the signed hash of the inputed message"

# adding the "padding" or extra characters to make the string an elligible block size
def pad(s):
	return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

# encrypt the string with AES256
def encrypt_message(key):
	# pad the string to the correct block_size
	messageToEncrypt = pad(message) 
	# intitialization vector to prevent repition in encryption
	# used to prevent repition & protects against dictionary attack
	iv = Random.new().read(AES.block_size)
	# create the actual cipher object to encrypt with
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# return the full, ciphertext version of the string 
	return iv + cipher.encrypt(messageToEncrypt) 

file_3 = encrypt_message(symmetricKey)
f3 = open('file_3.txt','w')
f3.write(file_3)
f3.close()
print "file_3.txt contains the message encrypted with the symmetric key"