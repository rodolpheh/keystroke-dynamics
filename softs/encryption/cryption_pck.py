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


def file_dump(encrypted: bytes, file_name: str = 'dump.dump') -> str:
    """Sauve une chaine chiffré dans un fichier

    Ecriture de la chaine de caractère chiffrée dans un fichier.
    L'utilisateur renseigne au préalable un nom de fichier dans lequel
    effectuer l'action.
    Le fichier peut etre existant ou non.
    Sert de manière générale pour ecrire un contenu dans un fichier
    """
    with open(file_name, 'wb') as dump_file:
        dump_file.write(encrypted)
    return file_name


def file_read(file_name: str) -> bytes:
    """Extrait une chaine chiffrée d'un fichier

    Le fichier est ouvert pour extraire son contenu sous forme
    d'une chaine de caractère.
    """
    with open(file_name, 'rb') as saved_dump:
        binary_lines = saved_dump.read()

    return binary_lines


def aes_gen(init_vector: str, key: str) -> AES.AESCipher:
    """Obtenir un nouveau objet AES

    Fonction prenant en entrée une clé de chiffrement
    et un vecteur d'initialisation.
    La fonction retourne l'AES initialisé.
    """
    return AES.new(key, AES.MODE_CBC, init_vector)


def encrypt(message: bytes, aes: AES.AESCipher) -> bytes:
    """Chiffre une chaine d'octets

    Chiffrement d'une chaine codée sur un multiple de 16 octets.
    Le chiffrement est effectué à l'aide de l'AES, fourni au préalable.
    La fonction retourne donc la chaine chiffrée.
    Un Zero Padding est appliqué.
    """

    # Convert eventual not-bytes object to bytes
    message = pickle.dumps(message)
    # Convert sequence of bytes to acii-compatible sequence of bytes
    message = binascii.hexlify(message)

    # Crypto.Cipher.AES.AESCipher needs an ASCII string to work on
    message_str = message.decode('ascii')

    # Section with zero-padding logic
    length = len(message_str)
    # Adding a position for the header value
    length += 1

    # Calculating length of needed padding
    if (length % 16) != 0:
        complement_size = 16 - (length % 16)
    else:
        complement_size = 0

    # Header holds the size of added padding
    header = hex(complement_size)
    # Stripping leading "0x" by keeping only last char
    header = header[-1]

    # Creating padding ASCII string with zeros
    complement = "0" * complement_size

    # Merging header message and padding
    message_str = "".join([header, message_str, complement])

    # Encrypt zero-padded message
    return aes.encrypt(message_str)


def decrypt(message: bytes, aes: AES.AESCipher) -> bytes:
    """Déchiffre une chaîne d'octets

    Déchiffrement d'une chaine codée sur un multiple de 16 octets.
    Le déchiffrement est effectué à l'aide de l'AES, fourni au préalable.
    La fonction retourné donc la chaine déchiffré.
    """

    # Get ASCII string of decrypted data
    encrypted = aes.decrypt(message).decode()

    # Retrieve size of padding by parsing header
    header = int(encrypted[0], 16)

    # Retrieve only payload of encoded data by stripping header
    # and padding
    decrypted = encrypted[1:(len(encrypted)-header)]

    # Decoding data from ASCII binary representation
    decrypted_bytes = binascii.unhexlify(decrypted)

    # Returning bytes after pickle unserialization
    return pickle.loads(decrypted_bytes)
