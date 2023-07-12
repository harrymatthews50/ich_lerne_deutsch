##
from ich_lerne_deutsch import drills, word_classes
import tkinter as tk
from tkinter import filedialog
import pickle
def activate_button(drill, word_list):
    out = drill.filter_word_list(word_list)
    if len(out)==0:
        return "disabled"
    else:
        return "active"

def launch_exercise():
    root.destroy()
    drill = drill_defs[selection.get()][1]
    words = drill.filter_word_list(word_list)
    obj = drill()
    obj.words = words
    obj.launch_app()
##
drill_defs=[('Speicherkarten',drills.Flashcards),('Nomen Genus',drills.NounArticles),('Was ist das Wort\n auf Deutsch?',drills.GermanWordMeanings),('Partizip II',drills.PerfektForms),('Plural',drills.PluralForms)]
root = tk.Tk()
root.title('Ich lerne Deutsch')
root.withdraw()
file = filedialog.askopenfilename(title="Select a word batch",filetypes=[('pickle','*.p')])
with open(file,'rb') as f:
    word_list=pickle.load(f)
#word_list = [item for item in word_list if not isinstance(item,word_classes.Verb)]
selection = tk.IntVar()
selection.set(None)

fr = tk.Frame(root, bg='#cbd1cc')
fr.pack()
labels,drill_classes = zip(*drill_defs)
for val, txt in enumerate(labels):
            but = tk.Radiobutton(fr,
                                 text=txt,
                                 padx=20,
                                 variable=selection,
                                 command=launch_exercise,
                                 value=val)
            but.configure(state=activate_button(drill_classes[val],word_list))
            but.pack(side="top", fill='x')
root.deiconify()
root.eval('tk::PlaceWindow . center')
root.mainloop()
