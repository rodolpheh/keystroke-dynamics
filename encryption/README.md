# Encryption/Decryption Package Manual

*The file will evolve with the differents add of features       
Please, take care to read this file in order to understand the library working*

- **1 : Install**
- **2 : Function List**
- **3 : How to use this package**
- **4 : Encrytion of a data**
- **5 : Decryption of a data**

## 1 - Install

*Before the installation, make sure you correctly put the differents files in the right folder (your projet folder)*
For the installation, you just need do give the good rights and execute the "deploy.sh" file.   

```bash
cd ~/myprojectfolder/
cp ~/encryption/* .
chmod +x deploy.sh
./deploy.sh
```

It will create a Python environnement and it will install the needed packages, in order to use some features like the *AES 256*.     
The main packages are *"Pickle"* and *"PyCrypto"*.      
*Pickle* is used to open/close files and to read/write into that files. It is useful to save some data (*AES* parameters for exemple).        
*PyCrypto* will import all the necessary features in order to process to an encryption and a decryption. It includes the AES encrytion.     

## 2 - Function List

### a) string_gen Function

- **Arguments :** None
- **Return :** String *key*

Make a random generation of a string

The string is encoded in 16 bytes.      
This function is used in order to generate an encrytion key and an Initialisation Vector (IV).

How to use it :     

```python
iv = string_gen()

key = string_gen()
print(iv) # 'a12Ze34rT67yui89'
print(key) # '98iuy76Tr43eZ21a'
```

### b) encrypt_parameters Function

- **Arguments :** None
- **Return :** List *aesParam* = [iv, key]

Make a list generation.     
This list contains an encrytion key and an Initialisation Vector (IV), which are necessary for the AES256 encryption.   
This function also stores that data in a file (called "param" by default).

How to use it :     

```python
params = encrypt_parameters()
print(params) # ['a12Ze34rT67yui89','98iuy76Tr43eZ21a']
```

### c) file_dump Function

- **Arguments :** String *crypt*, String *file_name (optional argument)*
- **Return :** String file_name

Write a content in a file.      
The user give a message in argument of the function in order to write it in a file.     
The function also accepts a file name in argument, but this optional use is more recommanded for internals program processes (example : Store important data specific to a program).       
By default, the user is asked to enter a file name, in order to define where the data, will be stored.      
Defining a file name in argument, will bypass this ask.

How to use it : 

```python
file_dump(aesParam, 'param')# Writing parameters in 'param' file

file_dump('Read the Manual')# Enter the file name
```

### d) file_read Function

- **Arguments :** String *file_name*
- **Return :** List / String *binary_lines*

Read a file content and store it into a variable.   
This function returns a variable with differents types available (it depends of the kind of data read) (example : Bytes, String, List of String).

How to use it :    

```python
test = file_read('myFile')
print(test) # 'Some String'
```

### e) aes_gen Function

- **Arguments :** String *iv*, String *key*
- **Return :** AES *aes*

Make a generation of the AES256.        
This function takes in arguments a key and an Initialisation Vector (IV).       
It is necessary to encode that strings in 16 bytes, in order to don't have an error.

How to use it :     

```python
aes = aes_gen(iv, key)
print(aes) #'<Crypto.Cipher.AES.AESCipher object at 0x7f6fc47156a0>'
```

### f) encryption Function

- **Arguments :** String *message*, AES *aes*
- **Return :** Bytes String *encrypted_message*

Make an encryption of a message.        
The function takes in arguments, an AES (generated before) and a message, encoded on a multiple of 16 bytes.        
The return will be the encrypted string.

How to use it :   

```python
crypt = encryption(myString, aes)
print(crypt) # "b'\x99\xff\xb9\x9c\xdf\xfd\xc4\x91\xa5\xe4\xb3\xc6t\xc6\x0b\x19"
```

### g) decryption Function

- **Arguments :** String *message*, AES *aes*
- **Return :** Bytes String *decrypted_message*

Make an decryption of a message.        
The function takes in arguments, an AES (generated before) and a message, encoded on a multiple of 16 bytes.        
The return will be the decrypted string.

How to use it :   
  
```python
decrypt = decryption(crypt, aes)
print(decrypt) # "My decrypted string"
```

## 3 How to use it

To use the package, you need to import it into your python script.

```python
from test_pck import *
```

After that, each function can be called in your script with the following syntax : 

```python
params = encrypt_parameters()
```

## 4 - Encrytion of a data

*In order to encrypt a string, there is a list of command to execute :*

```python
letters = "AStringToEncrypt"
params = encrypt_parameters()

aes = aes_gen(params[0], params[1])
crypt = encryption(letters, aes)
print("Encrypted data")
print(crypt)
file_name = file_dump(crypt)
```

After the execution of this script, we obtain this test in a terminal : 

```
python script.py     
Data : AStringToEncrypt     
Encrypted data      
b's\xb5x\x95\xfe|\xe6\x8a\x8bX\x12,R%\xf3\x1f'      
File Name to save : test        
Saved Successfully
```

## 5 - Decryption of a data

*In order to decrypt a string, there is a list of command to execute too. For this demonstration, let's start with the previous results :*

```python
binary_lines = file_read(file_name)
print("String Read")
print(binary_lines)
aes = aes_gen(params[0], params[1])
decrypt = decryption(binary_lines, aes)
print("Decrypted Data")
print(decrypt)
```
After the exection of this script, we obtain this result in a terminal : 

```
String Read        
b'\xbc\x0c\x8f6\n\x98^\x16K\xef\x94\xc2\~r%O'       
Crypted data :      
b'\xbc\x0c\x8f6\n\x98^\x16K\xef\x94\xc2\~r%O'        
Decrypted Data      
b'AStringToEncrypt'
```
