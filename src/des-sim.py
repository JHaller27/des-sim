# Author: James Haller
from encrypter import Encrypter
from key_scheduler import KeyScheduler

import logging

log = logging.getLogger('des-sim')
log.setLevel(logging.NOTSET)  # NOTSET, DEBUG, INFO
hand = logging.StreamHandler()
log.addHandler(hand)

def main():
    key = input('key > ')
    ks = KeyScheduler(key)

    plaintext = input('pt  > ')
    print()

    encrypter = Encrypter(ks)
    ciphertext = encrypter.encrypt(plaintext)

    print(ciphertext)


if __name__ == '__main__':
    main()
