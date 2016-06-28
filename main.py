# -*- coding: utf-8 -*-
import argparse
import getopt
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="The eternity corolle rotator")

    parser.add_argument("files_path", metavar="input-file", type=str, nargs='+', help="The file path")
    parser.add_argument("-o", "--output", metavar="output-file", type=str, nargs=1,
                        help="Output file path")
    parser.add_argument("-r", "--rotation", metavar="rotation", choices=[0, 1, 2, 3], type=int,
                        nargs=1,
                        help="the rotation to create")

    args = parser.parse_args()
    # Opening the file
    if args.output is not None and args.rotation is None:
        parser.print_help()
        sys.exit(0)
    for file_path in args.files_path:
        if args.rotation is not None:
            do_rotation(file_path, args.output, args.rotation[0])
        else:
            for i in xrange(4):
                print i
                do_rotation(file_path, None, i)


def do_rotation(file_in_path, file_out_path, rotation):
    dirname = os.path.dirname(file_in_path)

    file_in = open(file_in_path)
    # getting information from first 3 lines
    data_organisation = file_in.readline()  # ignored

    data = file_in.readline()  # getting information from file

    data_structure = file_in.readline()
    data_check = file_in.readline()

    data = data.split()
    del data[0]

    ori_rotation = int(data[1])
    hamming = int(data[6])
    nb_pieces = int(data[7])

    if ori_rotation == rotation:
        file_in.close()
        return
    rotation = (4 + (rotation - ori_rotation)) % 4

    if file_out_path is None:
        file_out_path = dirname + "/N(" + str(data[0]) + ")_C(" + str(rotation) + ")_P(" + data[2] + ":" + str(
            (int(data[3]) + rotation) % 4) + ")_Z(" + data[4] + "," + data[5] + ")_H(" + data[6] + ").txt"

    file_out = open(file_out_path, "w+")

    data[1] = str(rotation)
    new_data = "# " + " ".join(data) + "\n"

    file_out.write(data_organisation)
    file_out.writelines(new_data)
    file_out.write(data_structure)
    file_out.write(data_check)

    while 1:
        line_out = []
        lines = file_in.readlines(100000)
        if not lines:
            break
        for line in lines:
            line_out.append(";".join(generate(line.split(";"), hamming, rotation, nb_pieces)))
        file_out.writelines(line_out)

    file_in.close()
    file_out.close()


def generate(line, hamming, rotation, nb_pieces):
    """

    :param list line: the line
    :param int hamming:
    :param int rotation: how many rotations
    :param int nb_pieces:
    """
    pieces = line[:nb_pieces]
    colors = line[nb_pieces:]

    colors_shift = rotation * (hamming * 2 + 1)

    pieces_shift(pieces, hamming, rotation)
    pieces_rotate(pieces, rotation)
    color_shift(colors, colors_shift)
    return pieces + colors


def pieces_shift(pieces, hamming, how_much):
    for i in xrange(1, hamming + 1):
        shift(pieces, how_much * i, 2 * (i * (i - 1)) + 1, 2 * (i * (i + 1)))


def pieces_rotate(pieces, rotation):
    """

    :param list pieces:
    :param int rotation:
    """
    for i in xrange(len(pieces)):
        if pieces[i] != "-1":
            tmp = pieces[i].split(":")
            tmp[1] = str((int(tmp[1]) + rotation) % 4)
            pieces[i] = ":".join(tmp)


def color_shift(colors, colors_shift):
    """

    :param list colors:
    :param int colors_shift:
    :return:
    """
    shift(colors, colors_shift, end=len(colors) - 2)


def shift(lists, how_much, begin=0, end=-1):
    """

    :param list lists:
    :param int how_much:
    :param int begin:
    :param int end:
    """
    if end == -1:
        end = len(lists) - 1

    for i in xrange(0, how_much):
        lists.insert(begin, lists.pop(end))


def usage():
    print 'main.py file_path [-h, -o output_path, -r rotation]'


if __name__ == "__main__":
    main()
