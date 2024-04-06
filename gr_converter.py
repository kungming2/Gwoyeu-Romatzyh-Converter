# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
import csv

from _config import *


def vowel_neighbor(letter, word):
    """Checks a letter to see if vowels are around it."""
    vowels = 'aeiouy'

    for i in range(len(word)):
        if word[i] == letter:
            if i > 0 and word[i-1] in vowels:
                return True
            if i < len(word) - 1 and word[i+1] in vowels:
                return True
    return False


def vowel_preceder(letter, word):
    """Checks a letter to see if vowels precede it."""
    vowels = 'aeiouy'

    for i in range(len(word)):
        if word[i] == letter and i > 0 and word[i - 1] in vowels:
            return True
    return False



def zh_word_alt_romanization(pinyin_string):
    """
    Takes a pinyin with number item and returns version of it in the
    legacy Yale, Wade-Giles, and Gwoyeu Romatzyh romanization schemes.
    This is only used for zh_word at the moment.

    Example: Pinyin ri4 guang1 (日光) becomes:
    * jih^4 kuang^1 in Wade Giles.
    * r^4 gwang^1 in Yale.
    * ryhguang in GYRM.

    :param pinyin_string: A numbered pinyin string (e.g. pin1 yin1).
    :return: A tuple (Yale romanization, Wade-Giles, GYRM).
    """

    yale_list = []
    wadegiles_list = []
    gr_list = []

    # Save the corresponding pronunciations into a dictionary.
    corresponding_dict = {}
    csv_file = csv.reader(open(FILE_ADDRESS_ZH_ROMANIZATION, "rt",
                               encoding="utf-8"), delimiter=",")
    for row in csv_file:
        pinyin_p, yale_p, wadegiles_p, gr_p = row
        corresponding_dict[pinyin_p] = [yale_p.strip(), wadegiles_p.strip(), gr_p.strip()]

    # Divide the string into syllables.
    syllables = pinyin_string.split(' ')

    # Process each syllable.
    for syllable in syllables:
        tone = syllable[-1]
        syllable = syllable[:-1].lower()

        # Make exception for null tones.
        if tone is not "5":  # Add tone as superscript
            yale_equiv = "{}^({})".format(corresponding_dict[syllable][0], tone)
            wadegiles_equiv = "{}^({})".format(corresponding_dict[syllable][1], tone)
        else:  # Null tone, no need to add a number.
            yale_equiv = "{}".format(corresponding_dict[syllable][0])
            wadegiles_equiv = "{}".format(corresponding_dict[syllable][1])
        yale_list.append(yale_equiv)
        wadegiles_list.append(wadegiles_equiv)

    # Gwoyeu Romatzyh code. This is a complicated system, so it requires
    # a lot more work.
    for syllable in syllables:
        tone = int(syllable[-1])
        py_syllable = syllable[:-1].lower()

        # Break apart the initial and final from the original pinyin.
        # We keep them in pinyin for now.
        if py_syllable[0] in ('w', 'y'):
            initial = None
            final = py_syllable[1:]
        elif py_syllable[1] is 'h':
            initial = py_syllable[:1]
            final = py_syllable[2:]
        else:
            initial = py_syllable[0]
            final = py_syllable[1:]

        # Get the base GR syllable to modify.
        gr_base_syllable = corresponding_dict[py_syllable][2]
        gr_equiv = None

        # Modify based on tones.
        if tone == 1:
            # Tone 1
            if initial in ['l', 'm', 'n', 'r']:
                gr_equiv = f"{gr_base_syllable[0]}h{gr_base_syllable[1:]}"
            else:
                gr_equiv = gr_base_syllable
        elif tone == 2:
            # Tone 2
            if initial in ['l', 'm', 'n', 'r']:
                gr_equiv = gr_base_syllable
            elif 'i' in gr_base_syllable and final[-1] != 'i':
                gr_equiv = gr_base_syllable.replace('i', 'y')
            elif 'i' in gr_base_syllable and final[-1] == 'i':
                gr_equiv = gr_base_syllable.replace('i', 'y') + 'i'
            elif 'u' in gr_base_syllable and final[-1] != 'u':
                gr_equiv = gr_base_syllable.replace('u', 'w')
            elif 'u' in gr_base_syllable and final[-1] == 'u':
                gr_equiv = gr_base_syllable.replace('u', 'w') + 'u'
            else:
                last_vowel_index = -1
                for i, char in enumerate(gr_base_syllable):
                    if char in 'aeiou':
                        last_vowel_index = i
                if last_vowel_index != -1:
                    gr_equiv = gr_base_syllable[:last_vowel_index + 1] + 'r' + gr_base_syllable[last_vowel_index + 1:]
                else:
                    gr_equiv = gr_base_syllable
        elif tone == 3:
            # Tone 3
            if gr_base_syllable[0] in 'iu':
                if gr_base_syllable.startswith('i'):
                    gr_equiv = gr_base_syllable.replace('i', 'ye', 1)
                elif gr_base_syllable.startswith('u'):
                    gr_equiv = gr_base_syllable.replace('u', 'wo', 1)
            elif 'i' in gr_base_syllable and 'u' in gr_base_syllable:
                if gr_base_syllable.index('i') < gr_base_syllable.index('u'):
                    gr_equiv = gr_base_syllable.replace('i', 'e', 1)
                else:
                    gr_equiv = gr_base_syllable.replace('u', 'o', 1)
            elif 'i' in gr_base_syllable and vowel_neighbor('i', gr_base_syllable) and 'ei' not in gr_base_syllable:
                gr_equiv = gr_base_syllable.replace('i', 'e', 1)
            elif 'u' in gr_base_syllable and vowel_neighbor('u',
                                                            gr_base_syllable) and 'ou' not in gr_base_syllable and 'uo' not in gr_base_syllable:
                gr_equiv = gr_base_syllable.replace('u', 'o', 1)
            else:
                # The rules regarding doubling are complex.
                if 'uo' not in gr_base_syllable:
                    doubled = False
                    result = []
                    for char in gr_base_syllable:
                        if char in 'aeiouy' and not doubled:
                            result.append(char * 2)
                            doubled = True
                        else:
                            result.append(char)
                    gr_equiv = ''.join(result)
                else:
                    gr_equiv = gr_base_syllable.replace('o', 'oo')
        elif tone == 4:
            # Tone 4
            if 'i' in gr_base_syllable and vowel_preceder('i', gr_base_syllable):
                gr_equiv = gr_base_syllable.replace('i', 'y', 1)
            elif 'u' in gr_base_syllable and vowel_preceder('u', gr_base_syllable):
                gr_equiv = gr_base_syllable.replace('u', 'w', 1)
            elif gr_base_syllable.endswith('n') or gr_base_syllable.endswith('l'):
                gr_equiv = gr_base_syllable + gr_base_syllable[-1]
            elif gr_base_syllable.endswith('ng'):
                gr_equiv = gr_base_syllable.replace('ng', 'nq')
            else:
                gr_equiv = gr_base_syllable + 'h'

            # Separate check for null-onset.
            if gr_equiv.startswith('i'):

                if vowel_neighbor('i', gr_base_syllable):
                    gr_equiv = gr_equiv.replace('i', 'y', 1)
                else:
                    gr_equiv = "y" + gr_equiv
            elif gr_equiv.startswith('u'):
                if vowel_neighbor('u', gr_base_syllable):
                    gr_equiv = gr_equiv.replace('u', 'w', 1)
                else:
                    gr_equiv = "w" + gr_equiv
            if gr_equiv.endswith('iw'):
                gr_equiv = gr_equiv.replace('iw', 'iuh')
        elif tone == 5:
            # Neutral tone. No change.
            if py_syllable in ["me", "ge", "zi"]:
                # Abbreviation for -麼, -個, -子.
                gr_equiv = py_syllable[0]
            else:
                gr_equiv = str(gr_base_syllable)

        if gr_equiv:
            gr_list.append(gr_equiv)

    # Reconstitute the equivalent parts into a string.
    yale_post = " ".join(yale_list)
    wadegiles_post = " ".join(wadegiles_list)
    gr_post = "".join(gr_list)

    # Sole spelling exception: the Roma in GYRM:
    if "luomaa" in gr_post:
        gr_post = gr_post.replace("luomaa", "roma")

    return yale_post, wadegiles_post, gr_post


while True:
    entry_text = input("> Enter the Chinese pinyin to convert: ")

    print(zh_word_alt_romanization(entry_text)[2])
