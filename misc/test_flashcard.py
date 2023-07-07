##
import pickle
import tkinter as tk
from ich_lerne_deutsch import drills
# ##
# window = tk.Tk()
# window.config(padx=50, pady=50, bg='#FFFFFF')
# fr = drills.GermanTextEntry(window,width=200,height=200)
# fr.pack(side="left")
# w = drills.get_root_window(fr)
# assert(w==window)
# window.mainloop()
#


##



with open('../ich_lerne_deutsch/data/common_nouns.p','rb') as p:
    nouns = pickle.load(p)

from tkinter import *


##
import numpy as np
selection = []
for i in range(1000):
    selection.append(FS.select_next_trial())

selection = np.array(selection)
props = np.zeros(10)
for i in range(10):
    props[i] = sum(selection==i)/len(selection)



