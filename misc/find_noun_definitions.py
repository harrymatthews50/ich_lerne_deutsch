##
import pickle
from ich_lerne_deutsch.helpers import parse_entry_text_dictionary
import os
import numpy as np
from tqdm import tqdm
os.chdir('/Users/hmatth5/Documents/Projects/ich_lerne_deutsch')

with open('./ich_lerne_deutsch/data/nouns.p','rb') as p:
    nouns = pickle.load(p)
# read dictionary to try to get definitions
with open('./ich_lerne_deutsch/data/cdgdokbngm-871445221-7o898o.txt','r') as p:
    dict_entries = p.readlines()

##
parsed_entries = []
#dict_entries = [dict_entries[65652]]
for i,item in enumerate(dict_entries):
    parsed_entries.append(parse_entry_text_dictionary(item))

wort,theme,definition,gender = zip(*parsed_entries)
wort = np.array(wort)
theme = np.array(theme)
definition = np.array(definition)
gender = np.array(gender)
##
#keys = [item for item in nouns.keys()]
#nouns = {key: nouns[key] for key in ['Apfel','Kind','Buch','Zeitung']}
keys = [item for item in nouns.keys()]
unmatched = []
count = -1
for key, obj in tqdm(nouns.items()):
    count+=1
    matches = (wort==key)*(gender==obj._gender)
    if sum(matches)==0:
        unmatched.append(wort)
        continue
    # going to assume that the first entry is the most common usage for now
    inds = np.nonzero(matches)[0]
    defi = definition[inds[0]]
    if len(inds)>1:
        alt_defs =list(definition[inds[1:]])
    else:
        alt_defs = []
    obj._definition = defi
    obj._alternative_definitions = alt_defs

with open('./ich_lerne_deutsch/data/nouns_with_defs.p', 'wb') as f:
    pickle.dump(nouns,f)
with open('./ich_lerne_deutsch/data/unmatched_nouns.p', 'wb') as f:
    pickle.dump(unmatched,f)

# for some very common nouns overwrite with single word definitions








##

