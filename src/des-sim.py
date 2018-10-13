# Author: James Haller
from encrypter import Encrypter
from key_scheduler import KeyScheduler


def main():
    key = input('key > ')
    plaintext = input('pt  > ')

    encrypter = Encrypter(KeyScheduler(key))
    ciphertext = encrypter.encrypt(plaintext)

    print(ciphertext)


if __name__ == '__main__':
    main()
