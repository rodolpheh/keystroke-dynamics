import pickle
import random
import string
from typing import List
from Crypto.Cipher import AES
import binascii


def string_gen() -> str:
    """Génération alétoire d'une chaine de caractères

    Fonction de génération aléatoire d'une chaine de caractères
    codée sur 16 octets.
    Utilisé par défaut comme générateur de clé de chiffrement
    et d'Initialisation Vector.

    :returns: chaine de caractères aléatoire sur 16 octets
    """
    key = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(16))
    return key


def encrypt_parameters() -> List[str]:
    """Génération d'un vecteur d'initialisation et d'une clé de chiffrement

    Fonction générant un tableau contenant une clé de chiffrement
    et un vecteur d'initialisation, nécessaire pour le chiffrement AES.
    Stockage de ces paramètres dans un fichier 'param'.
    """
    key = string_gen()
    init_vector = string_gen()
    aes = [init_vector, key]
    return aes


def file_dump(encrypted: bytes, file_name: str = 'dump.dump'):
    """Sauve une chaine chiffré dans un fichier

    Ecriture de la chaine de caractère chiffrée dans un fichier.
    L'utilisateur renseigne au préalable un nom de fichier dans lequel
    effectuer l'action.
    Le fichier peut etre existant ou non.
    Sert de manière générale pour ecrire un contenu dans un fichier
    """
    with open(file_name, 'wb') as dump_file:
        pickle.dump(encrypted, dump_file)
        return file_name


def file_read(file_name: str):
    """Extrait une chaine chiffrée d'un fichier

    Le fichier est ouvert pour extraire son contenu sous forme
    d'une chaine de caractère.
    """
    with open(file_name, 'rb') as saved_dump:
        binary_lines = pickle.load(saved_dump)
    return binary_lines


def aes_gen(init_vector: str, key: str) -> AES.AESCipher:
    """Obtenir un nouveau objet AES

    Fonction prenant en entrée une clé de chiffrement
    et un vecteur d'initialisation.
    La fonction retourne l'AES initialisé.
    """
    return AES.new(key, AES.MODE_CBC, init_vector)


def encrypt(message, aes: AES.AESCipher) -> bytes:
    """Chiffre un chaîne

    Chiffrement d'une chaine codée sur un multiple de 16 octets.
    Le chiffrement est effectué à l'aide de l'AES, fourni au préalable.
    La fonction retourne donc la chaine chiffré.
    Un Zero Padding est appliqué.
    """
    message = binascii.hexlify(pickle.dumps(message))
    message = message.decode('ascii')

    length = len(message)
    length += 1

    if (length % 16 )!= 0:
        complement_size = 16 - (length % 16)
    else:
        complement_size = 0

    header = hex(complement_size)[-1]
    complement = "0" * complement_size
    message = "".join([header, message, complement])
    length = len(message)
    return aes.encrypt(message)


def decrypt(message: bytes, aes: AES.AESCipher):
    """Déchiffre une chaîne

    Déchiffrement d'une chaine codée sur un multiple de 16 octets.
    Le déchiffrement est effectué à l'aide de l'AES, fourni au préalable.
    La fonction retourné donc la chaine déchiffré.
    """
    encrypted = aes.decrypt(message).decode()
    header = int(encrypted[0], 16)
    decrypted = encrypted[1:(len(encrypted)-header)]
    decrypted_bytes = binascii.unhexlify(decrypted)
    return pickle.loads(decrypted_bytes)
