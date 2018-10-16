# Author: James Haller
import sys

from encrypter import Encrypter
from key_scheduler import KeyScheduler

import logging

log = logging.getLogger('des-sim')
log.setLevel(logging.NOTSET)  # less detail -> NOTSET, INFO, DEBUG -> more detail
hand = logging.StreamHandler(sys.stdout)
log.addHandler(hand)


def main():
    key = input('key > ')
    ks = KeyScheduler(key)

    plaintext = input('pt  > ')

    encrypter = Encrypter(ks)
    ciphertext = encrypter.encrypt(plaintext)

    print(ciphertext)


if __name__ == '__main__':
    main()
