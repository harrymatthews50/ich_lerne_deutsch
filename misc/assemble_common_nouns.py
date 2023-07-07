##
import copy
import pickle
from ich_lerne_deutsch.helpers import parse_entry_text_dictionary
import os
import numpy as np
from tqdm import tqdm
import re
import collections
os.chdir('/Users/hmatth5/Documents/Projects/ich_lerne_deutsch')

with open('./ich_lerne_deutsch/data/nouns_with_defs.p','rb') as p:
    nouns = pickle.load(p)

with open('./ich_lerne_deutsch/data/2000_plus_common_nouns.csv','r') as p:
    ls = p.readlines()

##
ls = [item.replace('\n','').replace('–','').replace('~','').split('\xa0') for item in ls]
ls = [[item for item in l if item!=''] for l in ls]

# extract the english  single word definition
english = [re.findall('[a-zA-Z\u00E4\u00F6\u00FC\u00C4\u00D6\u00DC\u00df]+',item[0]) for item in ls]
english = [item[0] for item in english]
singular = [re.findall('[a-zA-Z\u00E4\u00F6\u00FC\u00C4\u00D6\u00DC\u00df]+',item[1]) for item in ls]
plural = [re.findall('[a-zA-Z\u00E4\u00F6\u00FC\u00C4\u00D6\u00DC\u00df]+',item[2]) for item in ls]
deutsch = [item[-1] for item in singular]
duplicates = [item for item, count in collections.Counter(deutsch).items() if count > 1]
duplicate_locs = dict()
for i in duplicates:
    duplicate_locs[i] = np.nonzero(np.array(deutsch)==i)[0]

##
common_nouns = dict()
keys = [item for item in nouns.keys()]
for i in range(len(singular)):
    singular_form = singular[i]
    if len(singular_form) == 2:
        art = singular_form[0]
        word = singular_form[1]
        if word in keys:
            # check the article matches
            obj = nouns[word]
            common_nouns[word] = copy.deepcopy(obj)
            try:
                assert (obj.definite_article == art.lower())
                common_nouns[word]._definition = english[i]
            except:
                ...




##
with open('./ich_lerne_deutsch/data/common_nouns.p','wb') as p:
    nouns = pickle.dump(common_nouns,p)
