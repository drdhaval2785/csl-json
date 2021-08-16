# coding=utf-8
""" python json_from_babylon.py dictcode
    e.g. python json_from_babylon.py mw
"""
import sys
import codecs
import json
import os
from collections import defaultdict
from collections import OrderedDict


if __name__ == "__main__":
    dictId = sys.argv[1]
    filein = os.path.join('..', 'cologne-stardict', 'production', dictId + '.babylon')
    fin = codecs.open(filein, 'r', 'utf-8')
    data = fin.read()
    fin.close()
    output = OrderedDict()
    output['name'] = dictId
    output['source'] = 'https://raw.githubusercontent.com/indic-dict/stardict-sanskrit/master/sa-head/en-entries/yates/yates.babylon'
    entries = data.split('\n\n')[:-1]
    print(len(entries))
    counter = 1
    hwdict = OrderedDict()
    textdict = OrderedDict()
    for entry in entries:
        [hwline, text] = entry.split('\n')
        hws = hwline.split('|')
        for hw in hws:
            if hw in hwdict:
                hwdict[hw] += ','+str(counter)
            else:
                hwdict[hw] = str(counter)
        textdict[str(counter)] = text
        print(counter)
        counter += 1
    output['data'] = OrderedDict()
    output['data']['words'] = hwdict
    output['data']['text'] = textdict
    fileout = os.path.join('ashtadhyayi.com', dictId + '.babylon')
    fout = codecs.open(fileout, 'w', 'utf-8')
    json.dump(output, fout, indent=4, ensure_ascii=False)
    fout.close()
