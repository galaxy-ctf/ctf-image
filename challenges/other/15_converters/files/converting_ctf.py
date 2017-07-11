#!/usr/bin/env python
import optparse
from shutil import copyfile


def main():
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()
    input_fname, output_fname, command = args

    if command == 'to_cat':
        copyfile('/flags/cat.jpeg', output_fname)
    elif command == 'to_octopus':
        copyfile('/flags/octopus.jpg', output_fname)
    elif command == 'to_dog':
        copyfile('/flags/dog.jpeg', output_fname)
    elif command == 'to_octocat':
        copyfile('/flags/octocat.jpeg', output_fname)
    elif command == 'to_leopard':
        copyfile('/flags/octo_leopard.png', output_fname)
    elif command == 'to_link':
        copyfile('/flags/octo_link.jpeg', output_fname)
    elif command == 'to_octowho':
        copyfile('/flags/octo_who.jpeg', output_fname)
    elif command == 'to_zorro':
        copyfile('/flags/octo_zorro.jpeg', output_fname)
    elif command == 'to_flag':
        with open(output_fname, 'w') as f:
            f.write('Congrats! Here is your flag: gccctf{converting_like_a_champ}')
    elif command == 'almost':
        with open(output_fname, 'w') as f:
            f.write('Nice Work, but it is not quite that easy, keep going to find your flag!')

if __name__ == "__main__":
    main()
