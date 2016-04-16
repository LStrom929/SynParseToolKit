# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:15:03 2016

@author: jcrpda & ls
"""

import re
import nltk
rfile = raw_input("Enter a .txt file to convert to .csv: ")
ofile = raw_input("Enter the output file name: ")

f = open(file)

sent_list = f.readlines()

word_list = []

def rep(string):
    # strip the slash between the token and its tag, without stripping slashes part of the word
     string = string[::-1]
     return string.replace("/", " , ", 1)[::-1]

for sentence in sent_list: # iterate over sentence
    sentence = sentence.split(" ")
    for word in sentence: # iterate over words in sentences
        if (word != "\n") and (word != "./.") and (word != ":/:") and (word != ",/,"):
            word_list.append(rep(word))

with open(ofile, 'a') as out_file:

    for i in range(len(word_list)+1):
        out_file.write(word_list[i])
        
out_file.close()

#while True:
#    line = f.readlines()
#    for string in line:
#        word = string.split(r".*/[A-Z][A-Z](.)")
#        print(word)
##    for w , t in tagline:
##        print(w + ", " + t)
#    if not line: break
#    print()