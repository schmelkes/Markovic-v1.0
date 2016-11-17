"""
File            markov.py
Author          (Adapted from C#) Rafael Silva Quiroz / Salvador Parra Rosas
email           sqrf@icloud.com
License	        educational use
Description     Markov Chains in music
"""

import random


class RootWord(object):
    Start = False
    End = False
    Word = None
    ChildCount = 0
    Children = dict()


class Child(object):
    Occurrence = 0
    Word = None


class MarkovChain(object):
    def __init__(self):
        self._start_index = list()
        self._Words = dict()

    @property
    def words(self):
        return self._Words

    def load(self, input_string, work_ending):
        s = input_string
        next_is_start = False
        i = 0
        while i < len(s):
            if s[i] == "":
                break
            s1 = s[i].lower()
            c = Child()
            if s1 in self._Words:  # Already Exists, add new child word or update count of existing child word
                if i < len(s) - 1:
                    w = self._Words[s1]
                    if next_is_start:
                        w.Start = True
                        next_is_start = False
                        self._start_index.append(s1)
                    if s[i + 1].lower() in w.Children:  # Exists, just update count
                        c = w.Children[s[i + 1].lower()]
                        c.Occurrence += 1
                        w.Children.pop(s[i + 1].lower(), None)
                    else:  # Doesn't Exist, add new word
                        c.Word = s[i + 1]
                        c.Occurrence = 1
                    w.ChildCount += 1
                    w.Children[s[i + 1].lower()] = c
                    self._Words.pop(s1, None)
                    self._Words[s1] = w
            else:  # New Word
                w = RootWord()
                w.Children = dict()
                if i == 0:
                    w.Start = True
                    self._start_index.append(s1)
                w.Word = s[i]
                if i < len(s) - 1:
                    c.Word = s[i + 1]
                    c.Occurrence = 1
                    w.Children[s[i + 1].lower()] = c
                    w.ChildCount = 1
                else:
                    w.End = True
                if s1 == work_ending and i > 0:
                    w.End = True
                    next_is_start = True
                elif next_is_start:
                    w.Start = True
                    next_is_start = False
                    self._start_index.append(s1)
                self._Words[s1] = w
            i += 1

    def load_twins(self, input_list, work_ending):
        self._start_index = list()
        self._Words = dict()
        s = input_list
        next_is_start = False
        i = 0
        while i < len(s) - 1:
            if s[i] == "":
                break
            s1 = s[i].lower() + " " + s[i + 1].lower()
            w = RootWord()
            c = Child()
            if s1 in self._Words:  # Already Exists, add new child word or update count of existing child word
                if i < len(s) - 2:
                    w = self._Words[s1]
                    if next_is_start:
                        w.Start = True
                        next_is_start = False
                        self._start_index.append(s1)
                    if s[i + 2].lower() in w.Children:  # Exists, just update count
                        c = w.Children[s[i + 2].lower()]
                        c.Occurrence += 1
                        w.Children.pop(s[i + 2].lower(), None)
                    else:  # Doesn't Exist, add new word
                        c.Word = s[i + 2]
                        c.Occurrence = 1
                    w.ChildCount += 1
                    w.Children[s[i + 2].lower()] = c
                    self._Words.pop(s1, None)
                    self._Words[s1] = w
            else:  # New Word
                w = RootWord()
                w.Children = dict()
                if i == 0:
                    w.Start = True
                    self._start_index.append(s1)
                w.Word = s[i] + " " + s[i + 1]
                if i < len(s) - 2:
                    c.Word = s[i + 2]
                    c.Occurrence = 1
                    w.Children[s[i + 2].lower()] = c
                    w.ChildCount = 1
                else:
                    w.End = True
                if s1 == work_ending:
                    w.End = True
                    next_is_start = True
                elif next_is_start:
                    w.Start = True
                    next_is_start = False
                    self._start_index.append(s1)
                self._Words[s1] = w
            i += 1

    def output(self):
        output_chain = ""
        w = self._Words[random.choice(self._start_index).lower()]
        output_chain = "\n".join(w.Word.split(' ')) + "\n"
        c = Child()
        a = list()
        pos = 0
        rnd = 0
        min_p = 0
        max_p = 0  # bigger slice for more occurrences
        while not w.End:  # generate a new random word starting with our initial word
            rnd = random.randint(1, w.ChildCount)
            pos = 0
            for key, value in w.Children.iteritems():
                c = w.Children[key]
                min_p = pos
                pos += c.Occurrence
                max_p = pos
                # La Ocurrencia influencia los valores de min, max (a traves de pos) y rnd introduce aleatoriedad
                if min_p <= rnd & max_p >= rnd:
                    output_chain += c.Word + "\n"
                    new_word = self.new_couple(c.Word.lower(), self._Words)
                    w = self._Words[new_word]
                    break
        return output_chain

    @staticmethod
    def new_couple(w, words):
        ss = [v for k, v in words.iteritems() if k.startswith(w)]
        rnd = random.randint(0, len(ss)-1)
        rnd_phrase = ss[rnd]
        return rnd_phrase.Word.lower()
