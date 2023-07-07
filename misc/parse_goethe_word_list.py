##
from ich_lerne_deutsch import word_classes, helpers
import pandas as pd
import numpy as np

with open('/Users/hmatth5/Documents/Projects/ich_lerne_deutsch/ich_lerne_deutsch/data/Goethe_A1_Wordlist.csv','r') as f:
    r = f.readlines()

nouns = []
for i in range(len(r)):
    l = r[i]
    l = l.split('\t')

    # get the word
    word = l[1]

    if (word[0:3] in ['der','die','das']) & (len(word)>3):
        info = helpers.get_noun_info(l)
        nouns.append(info)





    # write nouns to A1 wordlist
singular,plural,gender,sentence,definition = zip(*nouns)
data = np.hstack([np.array(gender)[:,np.newaxis], np.array(singular)[:,np.newaxis],np.array(plural)[:,np.newaxis],np.array(sentence)[:,np.newaxis],np.array(definition)[:,np.newaxis]])
out = pd.DataFrame(data=data)
out.columns = ['Gender', 'Singular','Plural','Sentence','Definition']
out.to_csv('/Users/hmatth5/Documents/Projects/ich_lerne_deutsch/ich_lerne_deutsch/csv_word_lists/A1_nouns.csv',sep='\t')
