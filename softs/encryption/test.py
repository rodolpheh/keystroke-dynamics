import pickle
from cryption_pck import encrypt_parameters, aes_gen, encrypt, decrypt
from cryption_pck import file_dump, file_read
from Sample import Sample


def entrypoint():
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

    # Now let's do it with a serialized object

    sample = Sample()
    print("Sample object to encrypt : {}".format(sample))

    key, init_v = encrypt_parameters()
    encrypted_sample = encrypt(sample, aes_gen(init_v, key))
    print("Encrypted Sample : {}".format(encrypted_sample))

    file_name = file_dump(encrypted_sample)
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

    from_file = file_read(file_name)
    print("Data loaded from file:")
    print(from_file)

    decrypted = decrypt(from_file, aes_gen(init_v_from_file, key_from_file))
    print("Decrypted: {}".format(decrypted))


if __name__ == '__main__':
    entrypoint()
