# Author: James Haller
from encrypter import Encrypter
from key_scheduler import KeyScheduler

import logging

log = logging.getLogger('des-sim')
log.setLevel(logging.DEBUG)  # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
hand = logging.StreamHandler()
log.addHandler(hand)

def main():
    key = input('key > ')
    plaintext = input('pt  > ')
    print()

    encrypter = Encrypter(KeyScheduler(key))
    ciphertext = encrypter.encrypt(plaintext)

    print(ciphertext)


if __name__ == '__main__':
    main()
