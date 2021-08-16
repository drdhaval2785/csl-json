# coding=utf-8
""" python generate_json.py dictcode
	e.g. python generate_json.py mw
"""
import sys
import codecs
import json
import os
from parseheadline import parseheadline

def parsedict(pathToDict):
	fin = codecs.open(pathToDict, 'r', 'utf-8')
	result = {}
	text = ''
	for lin in fin:
		if lin.startswith('<L>'):
			meta = parseheadline(lin)
			lnum = meta['L']
			headword = meta['k1']
			text = lin
		elif lin.startswith('<LEND>'):
			result[lnum] = {'text': text, 'headword': headword}
		else:
			text += lin
	return result
	
if __name__ == "__main__":
	dictionary = sys.argv[1]
	dictionary = dictionary.lower()
	pathToDict = os.path.join('..', 'csl-orig', 'v02', dictionary, dictionary + '.txt')
	dictdata = parsedict(pathToDict)
	outputfolder = os.mkdir(dictionary)
	for k, v in dictdata.items():
		outputfile = os.path.join(dictionary, k + '.json')
		with codecs.open(outputfile, 'w', 'utf-8') as jsonfile:
			json.dump(v, jsonfile)

