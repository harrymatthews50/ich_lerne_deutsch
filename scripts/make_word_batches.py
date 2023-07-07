##
import tkinter as tk
from tkinter import filedialog, simpledialog
from ich_lerne_deutsch import word_classes
import pandas as pd
import numpy as np



root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title="Select word lists",filetypes=[('csv','*.csv')])
root.destroy()

root=tk.Tk()
root.withdraw()
intUserInput = simpledialog.askinteger(title="", prompt="How many words to include per batch")
root.destroy()
# detect what types of files they contain
## make word objects from each file

word_blocks = []

for f in file_paths:
    t = pd.read_csv(f,sep='\t')
    if t.columns[0]=='Inf':
        l = []
        for i in range(len(t)):
            l.append(word_classes.Verb(t.iloc[i,t.columns.get_loc("Inf")],t.iloc[i,t.columns.get_loc("Definition")],t.iloc[i,t.columns.get_loc("Perfekt Hilfsverb")]))

    elif t.columns[0] == 'Gender':
        l = []
        for i in range(len(t)):
            l.append(word_classes.Noun(t.iloc[i, t.columns.get_loc("Singular")],t.iloc[i, t.columns.get_loc("Gender")],plural_form=t.iloc[i,t.columns.get_loc("Plural")]))
    elif t.columns[0]=='Word':
            l = []
            for i in range(len(t)):
                l.append(word_classes.Word(t.iloc[i, t.columns.get_loc("Word")],t.iloc[i, t.columns.get_loc("Definition")]))
    word_blocks.append(l)
## sort into batches
# shuffle each word list
[np.random.shuffle(item) for item in word_blocks]

# get the relative proportions of each list
ns = np.array([len(item) for item in word_blocks])
batch_ns = np.ceil((ns/np.sum(ns))*intUserInput)

def save_batch(batch,batch_num,directory):
    ...


batch_num = 0
while True:
    batch = []
    for b in range(len(word_blocks)):
        for i in range(int(batch_ns[b])):
            batch.append(word_blocks[b].pop(0))

    save_batch(batch, batch_num, directory)
    if all([len(item)==0 for item in word_blocks]):
        break











