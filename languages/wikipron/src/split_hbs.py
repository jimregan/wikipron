#!/usr/bin/env python

import os
import logging

from codes import HBS_PATH


def _all_latin(word):
    try:
        word.encode("iso8859_2")
        return True
    except UnicodeEncodeError:
        return False


def _all_cyrillic(word):
    try:
        word.encode("iso8859_5")
        return True
    except UnicodeEncodeError:
        return False


def _split_file(path_prefix, path_affix, data):
    latin_count = 0
    cyrillic_count = 0
    latin_path = f"{path_prefix}latn_{path_affix}"
    cyrillic_path = f"{path_prefix}cyrl_{path_affix}"
    with open(latin_path, "w") as latin_file:
        with open(cyrillic_path, "w") as cyrillic_file:
            for line in data:
                word = line.split("\t", 1)[0]
                if _all_latin(word):
                    print(line.rstrip(), file=latin_file)
                    latin_count += 1
                    continue
                elif _all_cyrillic(word):
                    print(line.rstrip(), file=cyrillic_file)
                    cyrillic_count += 1
                    continue
                logging.info('"%s" is neither Latin nor Cyrllic.', word)
    if latin_count < 100:
        os.remove(latin_path)
        logging.info('"%s" contains less than 100 entires.', latin_path)
    if cyrillic_count < 100:
        os.remove(cyrillic_path)
        logging.info('"%s" contains less than 100 entires.', cyrillic_path)


# There is currently no hbs_phonetic.tsv
def main():
    phonetic_affix = "phonetic.tsv"
    phonemic_affix = "phonemic.tsv"

    try:
        with open(f"{HBS_PATH}{phonetic_affix}") as serb_croat_data:
            _split_file(HBS_PATH, phonetic_affix, serb_croat_data)
        os.remove(f"{HBS_PATH}{phonetic_affix}")
    except FileNotFoundError as err:
        logging.info("No Serbo-Croatian phonetic TSV: %s", err)

    try:
        with open(f"{HBS_PATH}{phonemic_affix}") as serb_croat_data:
            _split_file(HBS_PATH, phonemic_affix, serb_croat_data)
        os.remove(f"{HBS_PATH}{phonemic_affix}")
    except FileNotFoundError as err:
        logging.info("No Serbo-Croatian phonemic TSV: %s", err)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s %(levelname)s: %(message)s", level="INFO"
    )
    main()