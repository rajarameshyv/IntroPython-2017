#!/usr/bin/env python

infile = 'students.txt'

all_langs = []
with open(infile) as students:
    students.readline()
    for line in students:
        line = line.strip()
        langs = line.split(":")[1].split(",")
        if langs[0].strip()[0].isupper():
            langs = langs[1:]
        all_langs.extend(langs)

new_langs = [lang.strip() for lang in all_langs if lang.strip()]

all_langs = set(new_langs)
print(all_langs)

# a text file is an iterable
