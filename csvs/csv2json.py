#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Script for converting the new csv files to the desirable json format
'''
import codecs
import json
import re


def creeper():
    '''
    Settings for creeper file
    '''
    ccPrefix = False
    inFilename = u'creeper.csv'
    outFilename = u'Creeper.json'
    mappingFile = u'creeper-mappings.json'
    run(inFilename, outFilename, ccPrefix, mappingFile=mappingFile)


def mediaCreeper():
    '''
    Settings for mediaCreeper file
    '''
    ccPrefix = True
    inFilename = u'mediacreeper.csv'
    outFilename = u'MediaCreeper.json'
    run(inFilename, outFilename, ccPrefix)


def run(inFilename, outFilename, ccPrefix,
        mappingFile=None, source=u'http://b19.se/data/'):
    '''
    Run either file depending on settings
    '''
    # load mappings
    mappings = {}
    if mappingFile:
        f = codecs.open(mappingFile, 'r', 'utf-8')
        mappings = json.load(f)
        f.close()

    # load csv
    f = codecs.open(inFilename, 'r', 'ISO-8859-1')
    lines = f.read().split('\n')
    f.close()
    data = {}
    dates = []
    for l in lines:
        if len(l) == 0 or l.startswith(u'#'):
            continue
        start, end, cc, caption, updated = l.split(';')
        if ccPrefix:
            caption = u'[%s] %s' % (cc, caption)
        if caption in mappings.keys():
            caption = mappings[caption]
        if caption in data.keys():
            data[caption].append([start, end])
        else:
            data[caption] = [[start, end], ]
        dates.append(updated)

    # create metadata entry
    dates = sorted(list(set(dates)))
    metadata = {
        'source': source,
        'oldest data': dates[0],
        'newest data': dates[-1]}
    data[u'@metadata'] = metadata

    # output
    f = codecs.open(outFilename, 'w', 'utf-8')
    # f.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

    # compactify it without minimizing
    txt = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    txt = re.sub(
        r'\[\n            "([^"]*)", \n            "([^"]*)"\n        \]',
        r'["\1", "\2"]',
        txt)
    txt = txt.replace(u', \n        [', u',\n        [')
    f.write(txt)
    f.close()
