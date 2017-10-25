#!/usr/bin/env python

"""
parse students.txt file to get languages used students
"""

infile = "/Users/yaramati/Documents/GitProjects/PythonDevelopment/UWPCE/git/IntroPython-2017/examples/Session01/students.txt"

all_langs=[]
with open(infile,'r') as students:
	students.readline()
	for line in students:
		line = line.strip()
		langs = line.split(":")[1].split(",")
		if langs[0].strip()[0].isupper():
			langs = langs[1:]
		all_langs.extend(langs) 
		#print (langs)
		print (all_langs)