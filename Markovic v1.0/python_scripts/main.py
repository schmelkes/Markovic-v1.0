"""
File            main.py
Author          Rafael Silva Quiroz / Salvador Parra Rosas
email           sqrf@icloud.com
License	        educational use
Description     Markov Chains in music
"""


import os as os
from os.path import join as pjoin
import markov
from music21 import *


os.chdir("C:\Users\sqrf\Documents\markov\input")
#file_name = "mozart40-1.csv"
file_name = "beethoven5.csv"
#file_name = "bach1048-1.csv"


def create_note(n):
    switcher = {
        "S": "r"
    }
    return switcher.get(n, n.lower())


def create_duration(d):
    switcher = {
        "whole": "1",
        "half": "2",
        "quarter": "4",
        "eighth": "8",
        "16th": "16",
        "32th": "32"
    }
    return switcher.get(d, None)


with open(file_name, 'r') as data_file:
    reader = data_file.read().replace("\n", " ").replace("\t", " ").replace("  ", " ").split(' ')
    data = list(reader)
mc = markov.MarkovChain()

mc.load_twins(data, '.')
occurrences = list()

for key in mc.words:
    for c in mc.words[key].Children:
        occurrences.append('{:31}'.format(key) + '{:^10}'.format("-->") + '{:18}'.format(c) + '{:4}'.format(str(mc.words[key].Children[c].Occurrence)) + \
            '{percent:03.2%}'.format(percent=(float(mc.words[key].Children[c].Occurrence) / mc.words[key].ChildCount)))

print occurrences

output = mc.output()
score = ""
score += "4/4 "
for c in output.splitlines():
    l = c.split(',')
    score += create_note(l[0]) + create_duration(l[3]) + " "


newMarkov = tinyNotation.Converter(score)
stream1 = newMarkov.parse().stream
stream1.show('midi')
stream1.show()


output_filename = "new song"
path_to_file = pjoin("C:\Users\sqrf\Documents\markov\output", output_filename+".csv")
filetarget = open(path_to_file, "w")
filetarget.write("\n".join(map(lambda x: str(x), output.split())))
filetarget.close()

output_filename = "transition probabilities"
path_to_file = pjoin("C:\Users\sqrf\Documents\markov\output", output_filename+".txt")
filetarget = open(path_to_file, "w")
filetarget.write("\n".join(map(lambda x: str(x), occurrences)))
filetarget.close()



