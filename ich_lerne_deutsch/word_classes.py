import pandas as pd
import numpy as np
import copy as co
import tkinter as tk

class Word:
    def __init__(self, root_form, definition):
        self.root_form = root_form
        self._definition = definition

    @property
    def string(self):
        return self.root_form



class Verb:
    def __init__(self,infinitive_form,definition,perfekt_form=None,perfekt_hilfsverb=None):
        self.infinitive_form = infinitive_form
        self._definition = definition
        self.person = 3
        self.number = 'PLU'
        self.infinitive_form = infinitive_form
        self._definition = definition
        self.perfekt_form=perfekt_form
        if perfekt_hilfsverb is not None:
            if perfekt_hilfsverb not in ['sein','haben']:
                raise ValueError('Hilfsverb must be sein or haben. For word'+infinitive_form+' '+perfekt_hilfsverb + 'was given')
        self.prefekt_hilfsverb = perfekt_hilfsverb

    @property
    def string(self):
        return self.infinitive_form

class Adverb:
    def __init__(self, root_form, definition):
        self.root_form = root_form
        self._definition = definition

    @property
    def string(self):
        return self.root_form

#
# class Adjective:
#     def __init__(self, root_form, definition):
#         self.root_form = root_form
#         self._definition = definition
#
#     @property
#     def string(self):
 #       return self.root_form



class Noun:
    def __init__(self,root_form,gender,plural_form=None,plural_dative_form = None,genitive_form=None,definition = ''):
        self._root_form = root_form
        self._plural_form = plural_form
        self._plural_dative = plural_dative_form
        self._gender = gender
        self._number = 'SIN'
        self._case = 'NOM'
        if self._gender in ['MAS','NEU']:
            self._genitive_singular_form = genitive_form
        self._definition = definition
        self._alternative_definitions = []

    def __str__(self):
        definite_articles = np.zeros([4, 2], dtype=object)
        indefinite_articles = np.zeros([4, 2], dtype=object)
        negative_articles = np.zeros([4, 2], dtype=object)
        word_forms = np.zeros([4, 2], dtype=object)
        c = co.deepcopy(self)

        for row, case in enumerate(['NOM', 'AKK', 'DAT', 'GEN']):
            c._case = case
            for col, num in enumerate(['SIN', 'PLU']):
                c._number = num
                indefinite_articles[row, col] = c.indefinite_article
                definite_articles[row, col] = c.definite_article
                negative_articles[row, col] = c.negative_article
                word_forms[row, col] = c.string

        # make table of singular forms
        col = np.array(
            [definite_articles[i, 0] + '/' + indefinite_articles[i, 0] + '/' + negative_articles[i, 0] for i in
             range(4)])
        singular_forms = pd.DataFrame(index=['NOM', 'AKK', 'DAT', 'GEN'], columns=['Artikel', 'Wort'],
                                      data=np.hstack([col[:, np.newaxis], word_forms[:, 0][:, np.newaxis]]))
        col = np.array(
            [definite_articles[i, 0] + '/' + negative_articles[i, 0] for i in
             range(4)])

        plural_forms = pd.DataFrame(index=['NOM', 'AKK', 'DAT', 'GEN'], columns=['Artikel', 'Wort'],
                                    data=np.hstack([col[:, np.newaxis], word_forms[:, 1][:, np.newaxis]]))

        print([self._root_form+' ('+self.gender+'): '+self._definition])
        print('Singular forms...')
        print(singular_forms)
        print('')
        print('Plural forms ...')
        print(plural_forms)
        return ''

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self,value):
        if value not in ['SIN','PLU']:
            raise ValueError('Number must be SIN or PLU')
        self._number = value

    @property
    def case(self):
        return self._case

    @case.setter
    def case(self,value):
        if value not in ['NOM','AKK','DAT','GEN']:
            raise ValueError('Case must be in'+ str(['NOM','AKK','DAT','GEN']))
        self._case = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self,value):
        if value not in ['MAS','FEM','NEU','NOG']:
            raise ValueError()
        self._gender = value
    @property
    def definite_article(self):
        if (self.number is None) | (self.gender is None):
            return None
        if self.number == 'PLU':
            if self.case == 'NOM':
                return 'die'
            if self.case == 'ACC':
                return 'die'
            if self.case == 'DAT':
                return 'den'
            if self.case == 'GEN':
                return 'der'
        elif self.number == 'SIN':
            if self.gender == 'MAS':
                if self.case == 'NOM':
                    return 'der'
                if self.case == 'AKK':
                    return 'den'
                if self.case == 'DAT':
                    return 'dem'
                if self.case == 'GEN':
                    return 'des'
            elif self.gender == 'FEM':
                if self.case in ['NOM','AKK']:
                    return 'die'
                if self.case in ['DAT','GEN']:
                    return 'der'
            elif self.gender == 'NEU':
                if self.case in ['NOM','AKK']:
                    return 'das'
                if self.case == 'DAT':
                    return 'dem'
                if self.case == 'GEN':
                    return 'des'
            raise ValueError('Definite article not determined')

    @property
    def indefinite_article(self):
        if self.number == 'PLU':
            return ''
        elif self.number == 'SIN':
            if self.gender == 'MAS':
                if self.case == 'NOM':
                    return 'ein'
                if self.case == 'AKK':
                    return 'einen'
                if self.case == 'DAT':
                    return 'einem'
                if self.case == 'GEN':
                    return 'eines'
            if self.gender == 'FEM':
                if self.case in ['NOM','AKK']:
                    return 'eine'
                if self.case in ['GEN','DAT']:
                    return 'einer'
            if self.gender == 'NEU':
                if self.case in ['NOM', 'AKK']:
                    return 'ein'
                if self.case == 'DAT':
                    return 'einem'
                if self.case == 'GEN':
                    return 'eines'
        raise ValueError('Indefinite article not determined')



    @property
    def negative_article(self):
        if self.number == 'SIN':
            return 'k'+self.indefinite_article
        else:
            if self.case in ['NOM','AKK']:
                return 'keine'
            if self.case == 'DAT':
                return 'keinen'
            if self.case == 'GEN':
                return 'keiner'
        raise ValueError('indefinite article is not determined')


    @property
    def string(self):
        if self.number == 'SIN':
            if self.gender in ['MAS','NEU']:
                if self.case == 'GEN':
                    return self._genitive_singular_form
            return self._root_form
        if self.number == 'PLU':
            if self.case == 'DAT':
                return self._plural_dative
            return self._plural_form

    def get_all_possible_articles(self, cases = None):
        def_art = []
        indef_art = []
        neg_art = []
        if cases is None:
            cases = ["NOM","AKK","GEN","DAT"]
        c = co.deepcopy(self)
        for gender in ["MAS","FEM","NEU"]:
            for case in cases:
                c.gender = gender
                c.case = case
                def_art.append(c.definite_article)
                indef_art.append(c.indefinite_article)
                neg_art.append(c.negative_article)

        return set(def_art),set(indef_art),set(neg_art)
