# The following program generates an RSA key pair
from Crypto.PublicKey import RSA

key = RSA.generate(2048)

f1 = open('private_key.pem','w')
f2 = open('public_key.pem','w')

f1.write(key.exportKey('PEM'))

pub_key = key.publickey()

f2.write(pub_key.exportKey('PEM'))

f1.close()
f2.close()
