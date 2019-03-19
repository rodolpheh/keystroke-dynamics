import pickle
import random
from Crypto.Cipher import AES
import string
import struct

def string_gen():
    """Génération alétoire d'une chaine de caractères

    Fonction de génération aléatoire d'une chaine de caractères codée sur 16 octets.
    Utilisé par défaut comme générateur de clé de chiffrement et d'Initialisation Vector.
    """
    key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return key

def encrypt_parameters():
    """Génération d'un vecteur d'initialisation et d'une clé de chiffrement

    Fonction générant un tableau contenant une clé de chiffrement et un vecteur d'initialisation, nécessaire pour le chiffrement AES.
    Stockage de ces paramètres dans un fichier 'param'.
    """
    key = string_gen()
    iv = string_gen()
    aesParam=[iv, key]
    file_dump(aesParam, 'param')
    return aesParam

def file_dump(crypt, file_name=''):
    """Fonction de dump de fichier

    Ecriture de la chaine de caractère chiffré dans un fichier.
    L'utilisateur renseigne au préalable un nom de fichier dans lequel effectuer l'action.
    Le fichier peut etre existant ou non.
    Sert de manière générale pour ecrire un contenu dans un fichier
    """
    if file_name =='' :
        file_name = input('Entrez le nom de votre fichier : ')
    with open(file_name, 'wb') as file_dump:
        pickle.dump(crypt, file_dump)
        print("Saved Successfully")
        return file_name

def file_read(file_name):
    """Fonction de lecture d'un fichier

    Le fichier est ouvert pour extraire son contenu sous forme d'une chaine de caractère.
    """
    with open(file_name, 'rb') as saved_dump:
        binary_lines = pickle.load(saved_dump)
    return binary_lines

def aes_gen(iv, key):
    """Fonction de génération de l'AES

    Fonction prenant en entrée une clé de chiffrement et un vecteur d'initialisation.
    La fonction retourne en sortie, l'AES.
    """
    return AES.new(key, AES.MODE_CBC, iv)

def encryption(message, aes):
    """Fonction de chiffrement d'une chaine

    Chiffrement d'une chaine codée sur un multiple de 16 octets.
    Le chiffrement est effectué à l'aide de l'AES, fourni au préalable. La fonction retourné donc la chaine chiffré.
    """
    print("Data : "+message)
    return aes.encrypt(message)

def decryption(message, aes):
    """Fonction de déchiffrement d'une chaine

    Déchiffrement d'une chaine codée sur un multiple de 16 octets.
    Le déchiffrement est effectué à l'aide de l'AES, fourni au préalable. La fonction retourné donc la chaine déchiffré.
    """
    print("Crypted data : ")
    print(message)
    return aes.decrypt(message)