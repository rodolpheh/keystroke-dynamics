# Encryption/Decryption Package Manual

> *The file will evolve along the new features.
Please, take care to read this file in order to understand the library working*

## Contents

- [**1 - Install**](#1---Install)
- [**2 - Function List**](#2---Function-List)
- [**3 - How to use this package**](#3---How-to-use-this-package)
- [**4 - Encryption of data**](#4---Encryption-of-data)
- [**5 - Decryption of data**](#5---Decryption-of-data)

## 1 - Install

*Before the installation, make sure you correctly put the differents files in the right folder (your projet folder)*.
For the installation, you just need do add execution rigths to the script `deploy.sh`and execute it.

```bash
cd ~/myprojectfolder/
cp ~/encryption/* .
chmod +x deploy.sh
source ./deploy.sh
```

It will create a Python environement and it will install the needed packages, in order to use some features like the *AES 256*.

The main packages are `Pickle` and `PyCrypto`.
`Pickle` is used to open/close files and to read/write into that files. It is useful to save some data (*AES* parameters for exemple).
`PyCrypto` will import all the necessary features in order to process to an encryption and a decryption. It includes the AES encrytion.

## 2 - Function List

### a) `string_gen`

Generation of a random string.

The string is encoded on 16 bytes.
This function is used in order to generate an encryption key and an initialisation vector.

Usage:

```python
init_vector = string_gen()

key = string_gen()
print(init_vector) # e.g. 'a12Ze34rT67yui89'
print(key) # e.g. '98iuy76Tr43eZ21a'
```

### b) `encrypt_parameters`

Generates a pair of random strings.
This pair contains an encrytion key and an initialisation vector, which are necessary for the *AES256* encryption.

Usage:

```python3
params = encrypt_parameters()
print(params) # ['a12Ze34rT67yui89','98iuy76Tr43eZ21a']
```

### c) `file_dump`

Write a string to a file.

Usage:

```python
file_dump(crypted, 'param')# Writing parameters in 'param' file
```

### d) `file_read`

Read binary string from a file

Usage :

```python
test = file_read('my _file')
print(test) # 'Some String'
```

### e) `aes_gen`

Returns a AES object initialized with a key and an intialization vector.

Usage:

```python
aes = aes_gen(init_v, key)
print(aes) #'<Crypto.Cipher.AES.AESCipher object at 0x7f6fc47156a0>'
```

### f) `encrypt`

Encrypts a string.

Usage:

```python
crypt = encryption(a_string, aes)
print(crypt) # "b'\x99\xff\xb9\x9c\xdf\xfd\xc4\x91\xa5\xe4\xb3\xc6t\xc6\x0b\x19"
```

### g) `decrypt`

Decrytps a string.

The AES used for encryption should be **a newly generated `AES` object** with the **same parameters**. **DO NOT** use the same `AES` object, it won't work.

Usage:

```python
decrypt = decryption(crypt, aes)
print(decrypt) # "My decrypted string"
```

## 3 - How to use this package

### a) Import the package

```python
from cryption_pck import *
```

### b) Encryption of data

```python
letters = "AStringToEncrypt"
print("To encrypt : {}".format(letters.encode('ascii')))
key, init_v = encrypt_parameters()
aes = aes_gen(init_v, key)

crypted = encrypt(letters, aes)
print("Encrypted data : {}".format(crypted))
file_name = file_dump(crypted)

print("Data saved successfully to file \"{}\"".format(file_name))

# Save the key for later
aes_file = file_dump(str((init_v, key)), 'aes_key.key')
print("Key saved to file \"{}\"".format(aes_file))
```

After the execution of this script, we obtain this test in a terminal :

```txt
To encrypt : b'AStringToEncrypt'
Encrypted data : b'q\x0e\xcf\xe3\x9d>\x15d\x88u\xbf\xad2/\x9b\x82'
Data saved successfully to file "dump.dump"
Key saved to file "aes_key.key"
```

## 5 - Decryption of data

To decrypt a string, you must have the initalization vector and the key, and to create a new `AES` instance with the same parameters.

```python
init_v_from_file, key_from_file = ast.literal_eval(file_read('aes_key.key'))

from_file = file_read(file_name)
print("Data loaded from file:")
print(from_file)

decrypted = decrypt(from_file, aes_gen(init_v_from_file, key_from_file))
print("Decrypted: {}".format(decrypted))
```

After the exection of this script, we obtain this result in a terminal :

```txt
Data loaded from file:
b'\x9e_v\xe2M\x1en\xa4\x05\xa8\xb1\x02\x11\xe4O]'
Decrypted: b'AStringToEncrypt'
```
