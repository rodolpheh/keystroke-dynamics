import pickle
import random
from Crypto.Cipher import AES
import string
letters = "ABCDEFGHIJKLMNOP" #Doit etre un multiple de 16bits #list(string.ascii_letters)
key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
iv = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
print(iv)
aes = AES.new(key, AES.MODE_CBC, iv)
print(letters)
crypt = aes.encrypt(letters)
print(crypt)

#with open('test_pickle', 'wb') as file_dump:
#    pickle.dump(letters, file_dump)

#with open('test_pickle', 'rb') as saved_dump:
#  binary_lines = saved_dump.read()

#  print(binary_lines)
