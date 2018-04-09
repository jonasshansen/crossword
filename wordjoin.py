#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 08:35:25 2018

Load two lists of words and find common traits among them. This is especially
useful for the first four long words that form the edge of a crossword puzzle.

@author: Jonas Svenstrup Hansen <jonas.svenstrup@gmail.com>
"""

from scrape.wordscrape import wordscrape
import itertools

wordlist0 = wordscrape("p????????")
wordlist1 = wordscrape("????????m")


#common = [(word0, word1) for (word0, word1) in zip(wordlist0, wordlist1)
#	if word0[-1]==word1[0]]
#print(common)

wordproducts = itertools.product(wordlist0, wordlist1)

for wordproduct in wordproducts:
	word0, word1 = wordproduct
	if word0[-1] == word1[0]:
		print(wordproduct)
#common = [
#		(word0, word1) for (word0, word1) in
#		]