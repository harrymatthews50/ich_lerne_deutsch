import tkinter as tk
from tkinter import messagebox, ttk
from collections import OrderedDict
from abc import ABC, abstractmethod
import numpy as np
import copy as co
from ich_lerne_deutsch import word_classes
import time


class Drill(ABC):
    def __init__(self):
        super().__init__()
        self._words = None
        self._trial_history = None
        self._trial_num = -1
        self._prior_success_prob = .3
        self._prior_weight = 10
        self._remember_n_trials = 5
        self.n_trials = None
        self.n_successes = None
        self._window = None
        self._canvas = None
        self._canvas_items = []
        self._current_word = None
        self._current_word_id = None
        self._canvas_dimensions = None
        self._window_is_dead = True

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, val):
        self._words = val
        self.n_successes = np.zeros(len(val))
        self.n_trials = np.zeros(len(val))

    @property
    def success_probs(self):
        if (self.n_trials is None) | (self.n_successes is None):
            return None
        nS = self.n_successes + self._prior_success_prob * self._prior_weight
        nT = self.n_trials + self._prior_weight
        return nS / nT

    def select_next_trial(self):
        fail_prob = 1 - self.success_probs
        mini = np.min(fail_prob)
        # select candidates
        candidates = []
        while len(candidates) == 0:
            candidates = np.nonzero((np.random.uniform(0, 1, len(fail_prob)) - fail_prob) < 0)[0]
        if self._trial_history is not None:
            # find those that have recently well remembered
            recents = np.nonzero([np.all(item) for item in self._trial_history])[0]
            if len(recents) > 0:
                candidates = np.setdiff1d(candidates, recents)
                # add a tenth back in randomly
                candidates = np.concatenate(
                    (candidates, np.random.permutation(recents)[0:int(np.ceil(len(recents) / 10))]))

        return np.random.permutation(candidates)[0]

    def clear_canvas(self):
        n_ids = len(self._canvas_items)
        [self.clear_canvas_item(self._canvas_items.pop(0)) for i in range(n_ids)]

    def clear_canvas_item(self, item):
        if isinstance(item, (int, str)):
            self._canvas.delete(item)
        else:
            item.master.pack_forget()

    def set_new_word(self):
        self._current_word_id = self.select_next_trial()
        self._current_word = self.words[self._current_word_id]

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._window_is_dead = True
            self._window.destroy()

    def initialise_window_and_canvas(self):
        window = tk.Tk()
        window.config(padx=50, pady=50, bg='#FFFFFF')
        # get monitor resolution
        h = window.winfo_screenheight()
        w = window.winfo_screenwidth()
        window.protocol("WM_DELETE_WINDOW", self.on_closing)

        c_h = h * 0.5
        c_w = w * 0.5
        self._canvas_dimensions = (c_w, c_h)

        canvas = tk.Canvas(window, width=c_w, height=c_h)
        self._window = window
        self._canvas = canvas
        #  canvas.grid(row=0, column=0, columnspan=2)
        self._window_is_dead = False

    @abstractmethod
    def launch_app(self):
        ...


def key(event):
    print("pressed" + repr(event.char))


class NounFlashcards(Drill):
    def __init__(self):
        super().__init__()
        self.current_side = 1
        self.case = 'NOM'

    def launch_app(self):
        self.initialise_window_and_canvas()
        canvas = self._canvas
        canvas.bind('<Button-1>', self.next)
        canvas.focus_set()
        canvas.pack()
        self._window.mainloop()
        self.next()

    def next(self, event=None):
        if not self._window_is_dead:
            if self.current_side == 1:
                self.clear_canvas()
                self.set_new_word()
                self._canvas_items.extend(self.text_rehearsal_flashcard_side0())
                self.current_side = 0
            elif self.current_side == 0:
                self._canvas_items.extend(self.text_rehearsal_flashcard_side1())
                self.current_side = 1

    def text_rehearsal_flashcard_side1(self):
        # determine color given gender
        w = self._current_word
        if isinstance(w,word_classes.Noun):
            if w.gender == 'MAS':
                color = '#8289f5'
            elif w.gender == 'FEM':
                color = '#faafaf'
            elif w.gender == 'NEU':
                color = '#82f5a0'
            c = co.deepcopy(w)
            c.case = self.case
            c.number = 'SIN'
            sing_art = c.definite_article
            singular_text = c.string

            c.number = 'PLU'

            plur_art = c.definite_article
            plural_text = c.string
            self._canvas.configure(bg=color)
            self._canvas.itemconfig("singular", text=sing_art + ' ' + singular_text)
            try:
                self._canvas.itemconfig("plural", text=plur_art + ' ' + plural_text)
            except:
                ...

            definition = self._canvas.create_text(400, 63, text=w._definition, font=("Ariel", 60, "bold"),
                                                  tags="definition",
                                                  justify="center")
            self._canvas_items.append(definition)
            return [definition]

        elif isinstance(w, word_classes.Verb):
            definition = self._canvas.create_text(400, 63, text=w._definition, font=("Ariel", 60, "bold"),
                                                  tags="definition",
                                                  justify="center")

            if w.perfekt_hiflsverb=='haben':
                hv = 'hat'
            elif w.perfekt_hiflsverb=='sein':
                hv = 'ist'

            perfekt_text = 'Es '+hv +' '+ w.perfekt_form
            self._canvas.itemconfig("perfekt", text=perfekt_text)
            return [definition]

    def text_rehearsal_flashcard_side0(self):
        canvas = self._canvas
        texts = []
        if isinstance(self._current_word,word_classes.Noun):
            case = self.case
            c = co.deepcopy(self._current_word)
            c.case = case
            c.number = 'SIN'
            singular_text = c.string

            c.number = 'PLU'
            plural_text = c.string
            canvas.configure(bg='#A7A7A7')

            try:
                texts.append(
                    canvas.create_text(100, 163, text="___ " + singular_text + ' (Sg.)', font=("Ariel", 60, "bold"),
                                       tags="singular", justify="right", anchor="w"))
            except:
                print('Unable to display singular form')
            try:
                texts.append(canvas.create_text(100, 263, text="___ " + plural_text + '(Pl.)', font=("Ariel", 60, "bold"),
                                                tags="plural", justify="right", anchor="w"))
            except:
                print('Unable to display plural form')


        elif isinstance(self._current_word,word_classes.Verb):
            canvas.configure(bg='#A7A7A7')

            texts.append(
                canvas.create_text(100, 163, text=self._current_word.infinitive_form, font=("Ariel", 60, "bold"),
                                   tags="inf", justify="right", anchor="w"))
            texts.append(canvas.create_text(100, 263, text="Perfekt: ___  _________", font=("Ariel", 60, "bold"),
                                            tags="perfekt", justify="right", anchor="w"))

        return texts
class Test(Drill):
    def __init__(self):
        super().__init__()

    def update_scores(self, correct):
        self.n_trials[self._current_word_id] += 1
        if correct:
            self.n_successes[self._current_word_id] += 1
        self._trial_history[self._current_word_id].pop(0)
        self._trial_history[self._current_word_id].append(int(correct))
        self.update_progress_meter()

    def update_progress_meter(self):
        h = np.concatenate(self._trial_history)
        self.score.set((np.mean(h)) * 100)
        if self.score.get() == 100:
            self.create_congratulations_slide()
        print(self.score.get())

    def create_congratulations_slide(self):
        ...

    def initialise_window_and_canvas(self):
        super().initialise_window_and_canvas()
        self.score = tk.DoubleVar()
        self.score.set(0)

        self.progress_bar = ttk.Progressbar(self._window, orient="horizontal", mode="determinate", maximum=100,
                                            variable=self.score,length=self._canvas_dimensions[0]).pack(side="top")

        # initialise memory of previous trials
        self._trial_history = [co.deepcopy([0] * self._remember_n_trials) for i in range(len(self.words))]


class NounArticles(Test):
    def __init__(self):
        super().__init__()
        self.cases = ['NOM']

    def launch_app(self):
        self.initialise_window_and_canvas()
        canvas = self._canvas
        canvas.bind('<Button-1>', self.set_up_question_card)
        canvas.focus_set()
        canvas.pack()
        self._window.mainloop()

        self.set_up_question_card()

    def set_up_question_card(self, event=None):
        self.clear_canvas()
        self.set_new_word()
        self._canvas.configure(bg='#818281')

        case = self.cases[np.random.randint(0, len(self.cases))]
        type = 'definite article'

        # what is the text of the instructions
        instr_text = 'Select the correct ' + type + '.\n Case = ' + case + '.'

        # set up the info box
        d_art, id_art, neg_art = self._current_word.get_all_possible_articles(cases=self.cases)
        if type == 'definite article':
            arts = d_art
        elif type == 'indefinite article':
            arts = id_art
        elif type == 'negative article':
            arts = neg_art
        else:
            raise ValueError()

        arts = np.random.permutation(list(arts))

        self._response_int = tk.IntVar()
        self._response_int.set(None)
        self._response_strings = arts

        # add instruction text to canavs
        print(self._canvas.size())
        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, 0, text=instr_text, font=("Ariel", 30, "bold"),
                                     tags="definition",
                                     justify="center", anchor="n"))
        c = co.deepcopy(self._current_word)
        c.case = case
        c.number = 'SIN'
        singular_text = c.string

        if type == 'definite article':
            antword = c.definite_article
        elif type == 'indefinite article':
            antword = c.indefinite_article
        elif type == 'negative article':
            antword = c.negative_article
        else:
            raise ValueError()

        self._correct_answer = antword

        self._canvas_items.append(
            self._canvas.create_text(100, 163, text="___ " + singular_text + ' (Sg.)', font=("Ariel", 60, "bold"),
                                     tags="singular", justify="right", anchor="w"))

        fr = tk.Frame(self._window, bg='#cbd1cc')
        fr.pack()

        for val, txt in enumerate(arts):
            but = tk.Radiobutton(fr,
                                 text=txt,
                                 padx=20,
                                 variable=self._response_int,
                                 command=self.give_feedback,
                                 value=val)

            but.pack(side="left", fill='y')
        self._canvas_items.append(but)

    def give_feedback(self):
        given_answer = self._response_strings[self._response_int.get()]
        correct = given_answer == self._correct_answer
        self._is_correct = correct
        w = self._current_word
        if w.gender == 'MAS':
            color = '#8289f5'
        elif w.gender == 'FEM':
            color = '#faafaf'
        elif w.gender == 'NEU':
            color = '#82f5a0'

        # configure feedback
        # color the background according to the gender of the noun
        self._canvas.configure(bg=color)
        # add text of the correct answer

        if correct:
            text_color = '#05f545'
        else:
            text_color = '#fc3f3f'

        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, 200, text=self._correct_answer,
                                     font=("Ariel", 70, "bold"),
                                     tags="singular", justify="right", anchor="n", fill=text_color))

        self._canvas.bind('<Button 1>', self.next)

    def next(self, event=None):
        self.update_scores(self._is_correct)
        #    self._trial_num+=1
        self.set_up_question_card()

class WritingTest(Test):
    def __init__(self):
        super().__init__()

    def initialise_window_and_canvas(self):
        super().initialise_window_and_canvas()
        canvas = self._canvas
        fr = GermanTextEntry(self._window)
        fr.pack(side="bottom")
        self.text_entry = fr
        canvas.focus_set()
        canvas.pack()

    def set_new_word(self):
        super().set_new_word()
        self.text_entry.text.set('')

    def give_feedback(self, event=None):
        given_answer = self.text_entry.text.get()
        correct = given_answer.lower() == self._correct_answer.lower()
        self._is_correct = correct
        if correct:
            text_color = '#05f545'
        else:
            text_color = '#fc3f3f'

        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2,self._canvas_dimensions[1]/1.5, text=self._correct_answer,
                                     font=("Ariel", 70, "bold"),
                                     tags="singular", justify="right", anchor="n", fill=text_color))
        self.update_scores(correct)
        self._window.bind("<Return>", self.set_up_question_card)

    @abstractmethod
    def set_up_question_card(self):
        ...



class PluralForms(WritingTest):
    def __init__(self):
        super().__init__()
        self.cases = ["NOM"]
        self._remember_n_trials = 3

    def launch_app(self):
        self.initialise_window_and_canvas()
        self.set_up_question_card()
        self._window.mainloop()

    def set_up_question_card(self, event=None):
        self.clear_canvas()
        self.set_new_word()
        self._canvas.configure(bg='#818281')
        case = self.cases[np.random.randint(0, len(self.cases))]
        type = ['plural form', 'singular form'][np.random.randint(2)]

        # what is the text of the instructions
        instr_text = 'Enter the correct ' + type + ' with definite article.\n Then press Return/Enter.\n Case = ' + case + '.'
        # add instruction text to canavs
        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, 0, text=instr_text, font=("Ariel", 30, "bold"),
                                     tags="definition",
                                     justify="center", anchor="n"))
        c = co.deepcopy(self._current_word)
        c.case = case
        if type == 'plural form':
            c.number = 'SIN'
            text = c.string
            article = c.definite_article
            suffix = '(Sg.)'
            c.number = 'PLU'
            antword = c.definite_article + ' ' + c.string
        elif type == 'singular form':
            c.number = 'PLU'
            text = c.string
            article = c.definite_article
            suffix = '(Pl.)'
            c.number = 'SIN'
            antword = c.definite_article + ' ' + c.string
        else:
            raise ValueError()
        self._correct_answer = antword
        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, self._canvas_dimensions[1]/3, text=article + ' ' + text + ' ' + suffix, font=("Ariel", 60, "bold"),
                                     tags="singular", justify="right", anchor="n"))
        self._window.bind("<Return>", self.give_feedback)

class PerfektForms(WritingTest):
    def __init__(self):
        super().__init__()
        self.cases = ["NOM"]
        self._remember_n_trials = 3

    def launch_app(self):
        self.initialise_window_and_canvas()
        self.set_up_question_card()
        self._window.mainloop()

    def set_up_question_card(self, event=None):
        self.clear_canvas()
        self.set_new_word()
        self._canvas.configure(bg='#818281')
        case = self.cases[np.random.randint(0, len(self.cases))]

        instr_text = 'Complete the sentence in Perfekt form \n Es <Hilfsverb> <PartizipII>. \n for the verb\n'+self._current_word.infinitive_form
        # add instruction text to canavs
        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, 0, text=instr_text, font=("Ariel", 30, "bold"),
                                     tags="definition",
                                     justify="center", anchor="n"))

        if self._current_word.perfekt_hiflsverb == 'haben':
            hv = 'hat'
        elif self._current_word.perfekt_hiflsverb == 'sein':
            hv = 'ist'

        perfekt_text = 'Es ' + hv + ' ' + self._current_word.perfekt_form
        self._correct_answer = perfekt_text

        self._window.bind("<Return>", self.give_feedback)



class GermanWordMeanings(WritingTest):
    def __init__(self):
        super().__init__()
        self._remember_n_trials = 2

    def launch_app(self):
        self.initialise_window_and_canvas()
        self.set_up_question_card()
        self._window.mainloop()

    def set_up_question_card(self,event=None):
        self.clear_canvas()
        self.set_new_word()
        self._canvas.configure(bg='#818281')
        instr_text = 'Enter the correct German word\n if the word is a noun include the definite article\n assuming nominative case'
        # add instruction text to canavs
        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, 0, text=instr_text, font=("Ariel", 30, "bold"),
                                     tags="definition",
                                     justify="center", anchor="n"))

        c = co.deepcopy(self._current_word)
        definition = c._definition
        self._canvas_items.append(
            self._canvas.create_text(self._canvas_dimensions[0] / 2, self._canvas_dimensions[1]/3, text=definition, font=("Ariel", 60, "bold"),
                                     tags="definition", justify="right", anchor="n"))

        if isinstance(c,word_classes.Noun):
            c.case = 'NOM'
            c.number = 'SIN'
            antword = c.definite_article+' '+c.string
        elif isinstance(c,word_classes.Verb):
            antword = c.infinitive_form
        else:
            antword = c._root_form
        self._correct_answer = antword
        self._window.bind("<Return>", self.give_feedback)

class GermanTextEntry(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = tk.StringVar()
        self._character_codes = OrderedDict(
            [('a_uml', [[228, 196]]), ('o_uml', [[246, 214]]), ('u_uml', [[252, 220]]), ('ss', [[223]])])
        self.entry_widget = tk.Entry(self, textvariable=self.text)
        self.entry_widget.pack(side="top")
        button_panel = tk.Frame(self)
        but = tk.Button(button_panel, text=chr(self._character_codes['a_uml'][0][0]))
        but.bind("<Button-1>", lambda x: self.add_char(self._character_codes['a_uml'][0][0]))
        but.bind("<Shift-Button-1>", lambda x: self.add_char(self._character_codes['a_uml'][0][1]))
        but.pack(side="left")
        self._character_codes['a_uml'].append(but)

        but = tk.Button(button_panel, text=chr(self._character_codes['o_uml'][0][0]))
        but.bind("<Button-1>", lambda x: self.add_char(self._character_codes['o_uml'][0][0]))
        but.bind("<Shift-Button-1>", lambda x: self.add_char(self._character_codes['o_uml'][0][1]))
        but.pack(side="left")
        self._character_codes['o_uml'].append(but)

        but = tk.Button(button_panel, text=chr(self._character_codes['u_uml'][0][0]))
        but.bind("<Button-1>", lambda x: self.add_char(self._character_codes['u_uml'][0][0]))
        but.bind("<Shift-Button-1>", lambda x: self.add_char(self._character_codes['u_uml'][0][1]))
        but.pack(side="left")
        self._character_codes['u_uml'].append(but)

        but = tk.Button(button_panel, text=chr(self._character_codes['ss'][0][0]))
        but.bind("<Button-1>", lambda x: self.add_char(self._character_codes['ss'][0][0]))
        but.pack(side="left")
        self._character_codes['ss'].append(but)
        w = get_root_window(self)
        w.bind('<KeyPress-Shift_L>', self.shift_pressed)
        w.bind('<KeyRelease-Shift_L>', self.shift_released)
        w.bind('<KeyPress-Shift_R>', self.shift_pressed)
        w.bind('<KeyRelease-Shift_R>', self.shift_released)
        button_panel.pack(side="bottom")

    def shift_pressed(self, event=None):
        for key in self._character_codes.keys():
            item = self._character_codes[key]
            if len(item[0]) > 1:
                item[1].configure(text=chr(item[0][1]))

    def shift_released(self, event=None):
        for key in self._character_codes.keys():
            item = self._character_codes[key]
            if len(item[0]) > 1:
                item[1].configure(text=chr(item[0][0]))

    def add_char(self, char):
        self.entry_widget.insert(tk.INSERT, chr(char))


def get_root_window(child):
    elder = child
    while elder.master is not None:
        elder = elder.master
    return elder
