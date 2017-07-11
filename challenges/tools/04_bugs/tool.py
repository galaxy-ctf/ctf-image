#!/usr/bin/env python
import argparse
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

def e():
    raise Exception("")

def d(a):
    return e()

def c(arg=1):
    return d("gccctf{bu9_rep0rts_ev3rywh3re}")

def b(z, q=43):
    return c()

def a():
    return b(3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    args = parser.parse_args()

    a()
