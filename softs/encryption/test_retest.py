from cryption_pck import *
import pickle
from Sample import Sample


letters = "N'awak j'écris nawak tavu @ùù***$à~é&`§¤mqdsk"
print("Str to encrypt : \"{}\"".format(letters))

key, init_v = encrypt_parameters()
aes = aes_gen(init_v, key)

encrypted_letters = encrypt(letters, aes)
print("Encrypted str : {}".format(encrypted_letters))

file_name = file_dump(encrypted_letters)
print("Data saved successfully to file \"{}\"".format(file_name))

# Save the key for later
aes_filename = "key.key"
with open(aes_filename, 'wb') as keyfile:
    pickle.dump((init_v, key), keyfile)

print("Key saved to file \"{}\"".format(aes_filename))

with open(aes_filename, 'rb') as keyfile:
    ret = pickle.load(keyfile)
    init_v_from_file, key_from_file = ret
from_file = file_read(file_name)

print("Data loaded from file:")
print(from_file)

decrypted = decrypt(from_file, aes_gen(init_v_from_file, key_from_file))
print("Decrypted: {}".format(decrypted))
