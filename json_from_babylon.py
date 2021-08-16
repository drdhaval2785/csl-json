# coding=utf-8
""" python json_from_babylon.py dictcode
    e.g. python json_from_babylon.py mw
    Dr. Dhaval Patel
    16 August 2021
"""
import sys
import codecs
import json
import os
from collections import OrderedDict


if __name__ == "__main__":
    # Dictionary code
    dictId = sys.argv[1]
    # Read the production babylon.
    filein = os.path.join('..', 'cologne-stardict', 'production', dictId + '.babylon')
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.read()
    fin.close()
    # Initialize output dict
    # As the data of ashtadhyayi.com is in order, kept OrderedDict.
    output = OrderedDict()
    output['name'] = dictId
    output['source'] = 'https://raw.githubusercontent.com/sanskrit-lexicon/csl-json/main/ashtadhyayi.com/' + dictId + '.json'
    # Ignore the last one, as it will be an empty item.
    entries = data.split('\n\n')[:-1]
    # Total entries in the dictionary.
    print(len(entries))
    counter = 1
    # Initialize the dicts for headword and text.
    hwdict = OrderedDict()
    textdict = OrderedDict()
    # For each entry,
    for entry in entries:
        # Separate headword line and text line
        [hwline, text] = entry.split('\n')
        # Separate alternate headwords
        hws = hwline.split('|')
        # Attach the headword to ids.
        for hw in hws:
            # If headword is already there, append the id
            if hw in hwdict:
                hwdict[hw] += ','+str(counter)
            # Else, add the id de novo
            else:
                hwdict[hw] = str(counter)
        # Attach the text to id.
        textdict[str(counter)] = text
        # Print at 1000 entry interval for tracking progress.
        if counter % 1000 == 0:
            print(counter)
        # Increment
        counter += 1
    # Add the headword dict and text dict to the output.
    output['data'] = OrderedDict()
    output['data']['words'] = hwdict
    output['data']['text'] = textdict
    # Write to Json file.
    fileout = os.path.join('ashtadhyayi.com', dictId + '.json')
    fout = codecs.open(fileout, 'w', 'utf-8')
    json.dump(output, fout, separators=(',', ': '), indent=4, ensure_ascii=False)
    fout.close()
