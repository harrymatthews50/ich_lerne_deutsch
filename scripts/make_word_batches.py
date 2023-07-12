##
import tkinter as tk
from tkinter import filedialog, simpledialog
from ich_lerne_deutsch import word_classes
import pandas as pd
import numpy as np
import pickle
import os



root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title="Select word lists",filetypes=[('csv','*.csv')])


intUserInput = simpledialog.askinteger(title="", prompt="How many words to include per batch")

# detect what types of files they contain
## make word objects from each file

word_blocks = []

for f in file_paths:
    t = pd.read_csv(f,sep='\t')
    if t.columns[0]=='Inf':
        l = []
        for i in range(len(t)):
            l.append(word_classes.Verb(t.iloc[i,t.columns.get_loc("Inf")],t.iloc[i,t.columns.get_loc("Definition")],perfekt_hilfsverb=t.iloc[i,t.columns.get_loc("Perfekt Hilfsverb")],partizip_2 = t.iloc[i,t.columns.get_loc('Partizip_II')]))

    elif t.columns[0] == 'Gender':
        l = []
        for i in range(len(t)):

            singular = t.iloc[i, t.columns.get_loc("Singular")]
            plural = t.iloc[i,t.columns.get_loc("Plural")]
            definition =t.iloc[i,t.columns.get_loc("Definition")]
            if not isinstance(singular,str):
                singular = ''
            if not isinstance(plural,str):
                plural = ''
            if not isinstance(definition,str):
                definition = ''

            if singular=='':
                only_plural=True
            else:
                only_plural= False
            l.append(word_classes.Noun(singular,t.iloc[i, t.columns.get_loc("Gender")],definition=definition,plural_form=plural,only_plural=only_plural))
    elif t.columns[0]=='Word':
            l = []
            for i in range(len(t)):
                l.append(word_classes.Word(t.iloc[i, t.columns.get_loc("Word")],t.iloc[i, t.columns.get_loc("Definition")]))
    word_blocks.append(l)
# sort into batches
dst_folder=filedialog.askdirectory(parent=root)


# shuffle each word list
[np.random.shuffle(item) for item in word_blocks]

# get the relative proportions of each list
ns = np.array([len(item) for item in word_blocks])
batch_ns = np.ceil((ns/np.sum(ns))*intUserInput)

def save_batch(batch,batch_num,directory):
    with open(os.path.join(directory,'Batch'+str(batch_num)+'.p'),'wb') as p:
        pickle.dump(batch,p)


batch_num = 0
while True:
    batch = []
    for b in range(len(word_blocks)):
        for i in range(int(batch_ns[b])):
            if len(word_blocks[b])==0:
                break
            batch.append(word_blocks[b].pop(0))

    save_batch(batch, batch_num, dst_folder)
    batch_num += 1
    if all([len(item)==0 for item in word_blocks]):
        break











