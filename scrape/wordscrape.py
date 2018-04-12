#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 11:35:31 2018

@author: Jonas Svenstrup Hansen
"""
from lxml import html
import requests


def replace_chars(word):
	"""
	Replace search chars with website address equivalents.
	"""
	word = word.replace("?", "%3F")
	word = word.replace("#", "%23")
	word = word.replace("@", "%40")
	word = word.replace("æ", "%E6")
	word = word.replace("ø", "%F8")
	word = word.replace("å", "%E5")
	return word


def get_pagenum_from_words(pagenumber_words):
	num_pages = 1

	# Find the largest number in number_words:
	for word in pagenumber_words:
		try:
			pagenumber = int(word)
			if pagenumber > num_pages:
				num_pages = pagenumber
		except:
			pass
	return num_pages


def get_num_pages(websitename, websitebase, searchword):
	"""
	Get the number of web pages available.
	"""
	# Scrape website and structure in a tree:
	page = requests.get(websitename)
	tree = html.fromstring(page.content)

	# Get number of pages and other information from the tree:
	pagenumber_words = tree.xpath("//td/*/text()") # ...and some other words too

	# Find the largest number in number_words:
	num_pages = get_pagenum_from_words(pagenumber_words)

	pages_left = True
	while pages_left:
		if (num_pages == 10) or (num_pages > 10 and (num_pages-10) % 4 == 0):
			# Make new scraping of latest page:
			websitename = get_websitename(num_pages-1, websitebase, searchword)
			page = requests.get(websitename)
			tree = html.fromstring(page.content)
			pagenumber_words = tree.xpath("//td/*/text()")

			new_num_pages = get_pagenum_from_words(pagenumber_words)

			if new_num_pages <= num_pages:
				pages_left = False
			else:
				num_pages = new_num_pages
		else:
			pages_left = False

	return num_pages


def get_websitename(pagenum, websitebase, searchword):
	websitebase = "http://kryds.onlineordbog.dk/orcapia.cms?aid=213&"
	return websitebase + "start={}".format(pagenum) + "&w=" + searchword

def get_websitenames(num_pages, websitebase, searchword):
	"""
	Get the website names for all pages.
	"""
	websitenames = []

	for page in range(num_pages):
		websitenames.append(get_websitename(page, websitebase, searchword))

	return websitenames


def contains_newline(s):
	return "\n" in s

def contains_non_breaking_space(s):
	return "\xa0" in s

def mask_list(wordlist, filters):
	return [s for s in wordlist if not any(f(s) for f in filters)]


def wordscrape(searchword):
	"""
	Search the site http://kryds.onlineordbog.dk/ for a specific word and
	scrape the search results.
	It is currently assumed that there are less than 10 pages of words on
	the site.

	Parameters:
		searchword (string): Word to search for. Follows the search rules below.

	Returns:
		words (list of strings): All words that match the searchword.

	Search Rules (Danish):
		- ? (spørgsmålstegn) erstatter præcis ét tegn
		- \* (stjerne) ertatter nul eller flere tegn
		- # (kryds) erstatter en konsonant (gør søgning langsom)
		- @ (snabel-a) erstatter en vokal (gør søgning langsom)
	"""
	# Replace search chars with web address equivalents:
	searchword = replace_chars(searchword)

	# Set website address:
	websitebase = "http://kryds.onlineordbog.dk/orcapia.cms?aid=213&"
	websitename = websitebase + "w=" + searchword

	# Determine the number of pages on the web site:
	num_pages = get_num_pages(websitename, websitebase, searchword)

	# Get website names:
	if num_pages > 1:
		websitenames = get_websitenames(num_pages, websitebase, searchword)
	else:
		websitenames = [websitename]

	# Predefine words list:
	words = []

	# Find words on each page:
	for websitename in websitenames:
		# Scrape website and structure in a tree:
		page = requests.get(websitename)
		tree = html.fromstring(page.content)

		# Search for words:
		new_words = tree.xpath("//td/text()")

		# Filter out list elements that are not words:
		new_words = new_words[2:-1]
		filters = [contains_newline, contains_non_breaking_space]
		new_words_masked = mask_list(new_words, filters)

		# Add to word list:
		words.extend(new_words_masked)

	return words


if __name__ == "__main__":
	searchword = "?ern*"
	print("Searching for words that match: "+searchword)
	words = wordscrape(searchword)
	print(words)
