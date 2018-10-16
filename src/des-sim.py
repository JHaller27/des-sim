# Author: James Haller
import sys

from encrypter import Encrypter
from key_scheduler import KeyScheduler

import logging
import argparse

log = logging.getLogger('des-sim')
log.setLevel(logging.NOTSET)  # less detail -> NOTSET, INFO, DEBUG -> more detail
hand = logging.StreamHandler(sys.stdout)
log.addHandler(hand)


def main():
    parser = argparse.ArgumentParser(prog='des-sim.py')
    parser.add_argument("-v", "--verbosity", action="count",
                        help="verbosity of output (v, vv)")
    args = parser.parse_args()

    if args.verbosity is not None:
        if args.verbosity == 1:
            log.setLevel(logging.INFO)
        elif args.verbosity >= 2:
            log.setLevel(logging.DEBUG)

    key = input('key > ')
    ks = KeyScheduler(key)

    plaintext = input('pt  > ')

    encrypter = Encrypter(ks)
    ciphertext = encrypter.encrypt(plaintext)

    print(ciphertext)


if __name__ == '__main__':
    main()
