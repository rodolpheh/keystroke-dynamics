import pickle
import random
import string
from typing import List
from Crypto.Cipher import AES


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


def file_dump(encrypted_str: str, file_name: str = 'dump.dump'):
    """Sauve une chaine chiffré dans un fichier

    Ecriture de la chaine de caractère chiffrée dans un fichier.
    L'utilisateur renseigne au préalable un nom de fichier dans lequel
    effectuer l'action.
    Le fichier peut etre existant ou non.
    Sert de manière générale pour ecrire un contenu dans un fichier
    """
    with open(file_name, 'wb') as dump_file:
        pickle.dump(encrypted_str, dump_file)
        return file_name


def file_read(file_name: str):
    """Extrait une chaine chiffrée d'un fichier

    Le fichier est ouvert pour extraire son contenu sous forme
    d'une chaine de caractère.
    """
    with open(file_name, 'rb') as saved_dump:
        binary_lines = pickle.load(saved_dump)
    return binary_lines


def aes_gen(init_vector: str, key: str) -> AES:
    """Obtenir un nouveau objet AES

    Fonction prenant en entrée une clé de chiffrement
    et un vecteur d'initialisation.
    La fonction retourne l'AES initialisé.
    """
    return AES.new(key, AES.MODE_CBC, init_vector)


def encrypt(message: str, aes: AES) -> str:
    """Chiffre un chaîne

    Chiffrement d'une chaine codée sur un multiple de 16 octets.
    Le chiffrement est effectué à l'aide de l'AES, fourni au préalable.
    La fonction retourne donc la chaine chiffré.
    """
    return aes.encrypt(message)


def decrypt(message: str, aes: AES) -> str:
    """Déchiffre une chaîne

    Déchiffrement d'une chaine codée sur un multiple de 16 octets.
    Le déchiffrement est effectué à l'aide de l'AES, fourni au préalable.
    La fonction retourné donc la chaine déchiffré.
    """
    return aes.decrypt(message)
