import pickle
import random
from Crypto.Cipher import AES
import string
import struct

def encrypt_keygen():
    """Génération alétoire d'une clé de chiffrement

    Fonction de génération aléatoire d'une clé codée sur 16 octets
    Utilisé par défaut comme générateur de clé de chiffrement et d'Initialisation Vector
    """
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return key

def encrypt_ivgen():
    """Génération alétoire d'un vecteur d'initialisation

    Fonction de génération aléatoire d'un vecteur d'initialisation codé sur 16 octets
    Se repose sur la fonction de génération de clé de chiffrement
    """
    return encrypt_keygen()

def file_dump(crypt):
    """Fonction de dump de fichier

    Ecriture de la chaine de caractère chiffré dans un fichier
    L'utilisateur renseigne au préalable un nom de fichier dans lequel effectuer l'action
    Le fichier peut etre existant ou non
    """
    file_name = input('Entrez le nom de votre fichier : ')
    with open(file_name, 'wb') as file_dump:
        pickle.dump(crypt, file_dump)
        return file_name

def aes_gen(iv, key):
    """Fonction de dump de fichier

    Ecriture de la chaine de caractère chiffré dans un fichier
    L'utilisateur renseigne au préalable un nom de fichier dans lequel effectuer l'action
    Le fichier peut etre existant ou non
    """
    return AES.new(key, AES.MODE_CBC, iv)

def encryption(message, aes):
    print("Message initial : "+message)
    return aes.encrypt(message)

def decryption(message, aes):
    print("Message chiffré : ")
    print(message)
    return aes.decrypt(message)

letters = "Timothelegenie!!"

iv = encrypt_ivgen()
print("Initialisation vector :"+iv)
key = encrypt_keygen()
print("Encryption Key :"+key)
aes = aes_gen(iv, key)
crypt = encryption(letters, aes)
print("Données chiffrées")
print(crypt)
print(type(crypt))
file_name = file_dump(crypt)
with open(file_name, 'rb') as saved_dump:
    binary_lines = pickle.load(saved_dump)
print(binary_lines)
print(type(binary_lines))

aes = aes_gen(iv, key)

decrypt = decryption(crypt, aes)
print("Données déchiffré")
print(decrypt)
