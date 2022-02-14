# coding=utf-8
""" python json_from_babylon.py dictcode
    e.g. python json_from_babylon.py mw
    Dr. Dhaval Patel
    16 August 2021
    Prerequisite:
    1. csl-json repository is sibling of cologne-stardict repository.
    2. cologne-stardict has newest data in production folder.
    3. If you are not sure, it is better to run `bash redo.sh 1` in cologne-stardict repository, to ensure that the data is brought to the latest level.
"""
import sys
import codecs
import json
import os
import re
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
    entries = data.split('\n\n')[1:-1]
    # Total entries in the dictionary.
    print(len(entries))
    counter = 1
    # Initialize the dicts for headword and text.
    hwdict = OrderedDict()
    textdict = OrderedDict()
    # For each entry,
    for entry in entries:
        # Separate headword line and text line
        [hwline, t1] = entry.split('\n')
        t1 = re.sub('([^ \-])<BR>', '\g<1> <BR>', t1)
        t1split = t1.split('<BR>')
        text = ''.join(t1split[:-2])
        # <a href=\"https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=AP90&page=1196-b\" target=\"_blank\">Scan page : 1196-b</a>
        m = re.search('servepdf.php\?dict=(.+)&page=([^\"]+)"', t1split[-2])
        pc = m.group(2)
        # <a href=\"https://github.com/sanskrit-lexicon/csl-ldev/blob/main/v02/ap90/32175.txt\" target=\"_blank\">Correction submission : hemakUwa, 32175</a>
        n= re.search('blob/main/v02/([^/]+)/([^.]+)[.]txt"', t1split[-1])
        lnum = n.group(2)
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
        textdict[str(counter)] = [text, pc, lnum]
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
