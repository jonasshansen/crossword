#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 08:35:25 2018

Load two lists of words and find common traits among them. This is especially
useful for the first four long words that form the edge of a crossword puzzle.

@author: Jonas Svenstrup Hansen <jonas.svenstrup@gmail.com>
"""

import itertools
import argparse

from scrape.wordscrape import wordscrape


def wordjoin(wordlist0, wordlist1m, N0, N1):
	wordproducts = itertools.product(wordlist0, wordlist1)

	wordpairs = []

	for wordproduct in wordproducts:
		word0, word1 = wordproduct
		if word0[N0] == word1[N1]:
			wordpairs.append(wordproduct)

	return wordpairs


if __name__=="__main__":
	# Parse command line arguments:
	parser = argparse.ArgumentParser(description='Print a list of joined words.')
	parser.add_argument('word0', metavar='word0', help='First word to use')
	parser.add_argument('word1', metavar='word1', help='Second word to use')

	args = parser.parse_args()

	word0 = args.word0
	word1 = args.word1

	# Get common letter integers from & character position in words:
	N0 = word0.find('&')
	N1 = word1.find('&')

	# Replace standin common letter character:
	word0 = word0.replace('&','?')
	word1 = word1.replace('&','?')

	# Scrape website
	wordlist0 = wordscrape(word0)
	wordlist1 = wordscrape(word1)

	# Get wordpairs:
	wordpairs = wordjoin(wordlist0, wordlist1, N0, N1)
	if not wordpairs:
		print("No word pairs found.")
	else:
		for wordpair in wordpairs:
			print(wordpair)
