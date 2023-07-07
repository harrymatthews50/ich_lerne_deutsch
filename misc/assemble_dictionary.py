
##
import os
from ich_lerne_deutsch.word_classes import Noun
from tqdm import tqdm
import pickle

def get_gender(entry):
    g = [item[1][3] for item in entry]
    if len(set(g))==1:
        return g[0]
    else:
        raise ValueError('Multiple genders')

def is_number(entry,number):
    return [item[1][2] == number for item in entry]
def is_case(entry,case):
    return [item[1][1] == case for item in entry]
def is_not_case(entry,case):
    return [item==False for item in is_case(entry,case)]

def find_plural_form(entry):
    is_p = is_number(entry,'PLU')
    is_not_dative = is_not_case(entry,'DAT')
    for i in range(len(entry)):
        if is_p[i] & is_not_dative[i]:
            return entry[i][0]

    print('Could not find plural form')
    return None
def find_plural_dative_form(entry):
    is_p = is_number(entry, 'PLU')
    is_dative = is_case(entry, 'DAT')
    for i in range(len(entry)):
        if is_p[i] & is_dative[i]:
            return entry[i][0]
    print('Could not find plural dative')
    return None


def find_singular_genetive_form(entry):
    is_p = is_number(entry, 'SIN')
    is_dative = is_case(entry, 'GEN')
    for i in range(len(entry)):
        if is_p[i] & is_dative[i]:
            return entry[i][0]
    print('Could not find genitive singular')

def screen_item(item):
    if item == '-':
        return False
    if any([x in '0123456789' for x in item]):
        return False
    return True
def create_noun_object(dict_,key):
    root_form = key
    entry = dict_[key]
    gender = get_gender(entry)
    plural_form = find_plural_form(entry)
    if gender in ['MAS', 'NEU']:
        sing_gen = find_singular_genetive_form(entry)
    else:
        sing_gen = None
    plural_dative = find_plural_dative_form(entry)
    obj = Noun(root_form, gender, plural_form=plural_form, plural_dative_form=plural_dative, genitive_form=sing_gen)
    return obj

os.chdir('/Users/hmatth5/Documents/Projects/ich_lerne_deutsch')
with open('./ich_lerne_deutsch/data/dictionary.dump', 'r') as f:
    rs = f.readlines()

# parse the input

parsed_lines = [item.replace('\n','').split('\t') for item in rs if item[0] != '#']
word,root,tags = zip(*parsed_lines)
word=[item for item in word]
root = [item for item in root]
tags = [item.split(':') for item in tags]

keep =[screen_item(item) for item in word]
word = [word[i] for i in range(len(keep)) if keep[i]]
root = [root[i] for i in range(len(keep)) if keep[i]]
tags = [tags[i] for i in range(len(keep)) if keep[i]]




tag_1 =[item[0] for item in tags]
noun_inds = [item=='SUB' for item in tag_1]

# for each nound grab each form
improper_nouns = dict()

for i in range(len(noun_inds)):
    if noun_inds[i]:
        if root[i] not in improper_nouns:
            # initialise
            improper_nouns[root[i]] = [(word[i],tags[i])]
        else:
            improper_nouns[root[i]].append((word[i],tags[i]))

## sort it
noun_objects = dict()
keys = [item for item in improper_nouns.keys()]
for i in tqdm(range(len(keys))):
    try:
        noun_objects[keys[i]] = create_noun_object(improper_nouns,keys[i])
        improper_nouns.pop(keys[i])
    except:
        ...

with open('./ich_lerne_deutsch/data/nouns.p', 'wb') as f:
    pickle.dump(noun_objects,f)
with open('./ich_lerne_deutsch/data/problem_nouns.p', 'wb') as f:
    pickle.dump(improper_nouns,f)






##

