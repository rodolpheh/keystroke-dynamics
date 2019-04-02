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

Write bytes to a file.

Usage:

```python
# Writing parameters in 'param' file
file_dump(encrypted_message, 'param')
```

### d) `file_read`

Read bytes from a file

Usage :

```python
test = file_read('my _file')
print(test) # b'Some bytes'
```

### e) `aes_gen`

Returns a AES object initialized with a key and an intialization vector.

Usage:

```python
aes = aes_gen(init_v, key)
print(aes) #'<Crypto.Cipher.AES.AESCipher object at 0x7f6fc47156a0>'
```

### f) `encrypt`

Encrypts bytes.

Usage:

```python
crypt = encryption(some_bytes, aes)
print(crypt) # "b'\x99\xff\xb9\x9c\xdf\xfd\xc4\x91\xa5\xe4\xb3\xc6t\xc6\x0b\x19"
```

### g) `decrypt`

Decrypts bytes.

The AES used for encryption should be **a newly generated `AES` object** with the **same parameters**. **DO NOT** use the same `AES` object, it won't work.

Usage:

```python
decrypt = decryption(encrypted, aes)
print(decrypt) # b'Decrypted bytes'
```

## 3 - How to use this package

### a) Import the package

```python
from cryption_pck import *
```

### b) Encryption of data

```python
    letters = "A UTF-8 string ( ͡° ͜ʖ ͡°)"
    print("Str to encrypt : \"{}\"\n".format(letters))

    key, init_v = encrypt_parameters()
    aes = aes_gen(init_v, key)

    encrypted_letters = encrypt(letters, aes)
    print("Encrypted str : {}\n".format(encrypted_letters))

    file_name = file_dump(encrypted_letters)
    print("Data saved successfully to file \"{}\"\n".format(file_name))

    # Save the key for later
    aes_filename = "key.key"
    with open(aes_filename, 'wb') as keyfile:
        pickle.dump((init_v, key), keyfile)

    print("Key saved to file \"{}\"\n".format(aes_filename))
```

After the execution of this script, we obtain this test in a terminal :

```txt
Str to encrypt : "A UTF-8 string ( ͡° ͜ʖ ͡°)"

Encrypted str : b'J\x07b\xc2m3\x1axPv\xa1\xb6/\xfe\xee`\\\xfd\x97$\x97\xddi3q\x1e\xdfZ\x17l\x0f\xdb/\x88\x18\xbd\xa5\xc9\x87"\x87\xd1\x96\x83\xd8\xb0\x9d\t\xb7\xc2\xca\xb1\x9f\x83\xb5\n8\xb9G\xe4H\'#\x11\x94\xa1d4\xd6\x8f\xda+\x9e\xf4a\x14\x92\x10\xa9\xad\xa5X\xa1\xbfS\xaa\xa1\xfe\x8cs\x95b^\x17\xd2k'

Data saved successfully to file "dump.dump"

Key saved to file "key.key"
```

## 5 - Decryption of data

To decrypt data, you must have the initalization vector and the key, and to create a new `AES` instance with the same parameters.

```python
    with open(aes_filename, 'rb') as keyfile:
        ret = pickle.load(keyfile)
        init_v_from_file, key_from_file = ret

    from_file = file_read(file_name)
    print("Data loaded from file:")
    print(from_file)
    print()

    decrypted = decrypt(from_file, aes_gen(init_v_from_file, key_from_file))
    print("Decrypted: {}\n".format(decrypted))
```

After the exection of this script, we obtain this result in a terminal :

```txt
Data loaded from file:
b'J\x07b\xc2m3\x1axPv\xa1\xb6/\xfe\xee`\\\xfd\x97$\x97\xddi3q\x1e\xdfZ\x17l\x0f\xdb/\x88\x18\xbd\xa5\xc9\x87"\x87\xd1\x96\x83\xd8\xb0\x9d\t\xb7\xc2\xca\xb1\x9f\x83\xb5\n8\xb9G\xe4H\'#\x11\x94\xa1d4\xd6\x8f\xda+\x9e\xf4a\x14\x92\x10\xa9\xad\xa5X\xa1\xbfS\xaa\xa1\xfe\x8cs\x95b^\x17\xd2k'

Decrypted: A UTF-8 string ( ͡° ͜ʖ ͡°)
```

Note that it's the same logic with any Object. The API of this modules requires the data to already be a sequence of bytes.
You could use `pickle` as a serializor. [See `test.py`](test.py) for an example.
