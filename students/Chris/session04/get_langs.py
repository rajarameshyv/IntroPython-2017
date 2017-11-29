#!/usr/bin/env python

"""
parse students.txt file to get languages used by students
"""

infile = "students.txt"

all_langs = []
with open(infile, 'r') as students:
    students.readline()
    for line in students:
        line = line.strip()
        langs = line.split(":")[1].split(",")
        if langs[0].strip()[0].isupper():
            langs = langs[1:]
        all_langs.extend(langs)
        print(langs)

# new_langs = []
# for lang in all_langs:
#     if lang.strip():
#        new_langs.append(lang.strip())

new_langs = [lang.strip() for lang in all_langs if lang.strip()]

all_langs = set(new_langs)
print(all_langs)

