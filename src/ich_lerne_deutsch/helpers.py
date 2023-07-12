import re


def replace_text(string,prev, new):
    # find the last occurrence of the old text
    loc = string.rfind(prev)
    if loc == -1:
        raise ValueError()
    st = loc
    end = loc + len(prev)
    return string[:st] + new + string[end:]

def get_noun_info(split_text):
    word = split_text[1]
    article = word[0:3]
    word = word[4:]
    word = word.split(',')
    if len(word)>1:
        plural_signals = []
        for i in range(1,len(word)):
            plural_signals.extend(word[i].split(' '))
        plural_signals2 = []
        for i in range(1,len(plural_signals)):
            plural_signals2.extend(plural_signals[i].split(' '))
        plural_signals = plural_signals2
        plural_signals = [item.lower() for item in plural_signals if len(item)!=0]
        if '#pl' in plural_signals:
            only_plural = True
        else:
            only_plural = False
    else:
        plural_signals = ''
        only_plural= False
    word = word[0]
    if only_plural:
        gender = 'NOG'
        plural_form = word
        singular_form = None
    else:
        if article=='die':
            gender='FEM'
        elif article=='der':
            gender = 'MAS'
        elif article=='das':
            gender='NEU'

        singular_form=word
        plural_form=make_plural(singular_form,plural_signals)

    sentence = split_text[2]
    definition = split_text[3]
    return singular_form, plural_form, gender, sentence, definition


def make_plural(singular,plural_signals):
    def modify_noun(noun,signal):
        noun = noun.lower()
        # if noun=='datum':
        #     a=1
        signal = signal.lower()
        signal = signal.replace('-','')
        signal = signal.replace('–', '')
        if len(signal)==0:
            return noun
        if '→' in signal: # deal with irregular changes
            signal = signal.split('→')
            prev = signal[0]
            new = signal[1]
            return replace_text(noun,prev,new)
        elif signal == 'ü':
            prev = 'u'
            new = 'ü'
            return replace_text(noun, prev, new)
        elif signal == 'ä':
            prev = 'a'
            new = 'ä'
            return replace_text(noun, prev, new)
        elif signal == 'ö':
            prev = 'o'
            new = 'ö'
            return replace_text(noun, prev, new)

        return noun+signal
    plural = singular
    for i in range(len(plural_signals)):
        plural = modify_noun(plural,plural_signals[i])
    if plural != '':
        plural = plural[0].upper()+plural[1:]
    return plural









def parse_entry_text_dictionary(entry):
    if (entry[0] in '\'#&-0123456789') | (entry == '\n'):
        return None,None,None,None
    if entry[0:3] == '...':
        return None,None,None,None

    spl = entry.replace('\n', '').split('\t')
    deutsch = spl[0]
    theme_match = re.search('(?<=\().+?(?=\))', spl[0])
    if theme_match is not None:
        st, end = theme_match.regs[0]
        theme = theme_match.string[st:end]
        deutsch=deutsch[end:]
    else:
        theme = None

    # extract the word in German
    # if noun extract gender
    if spl[2] == 'noun':
        gender = re.search('(?<=\{).+?(?=\})',deutsch)
        if gender is None:
            gen = 'NOG'
        else:
            st, end = gender.regs[0]
            g = gender.string[st:end]
            deutsch = deutsch[:st-2]+deutsch[end+1:]
            if g == 'n':
                gen = 'NEU'
            elif g == 'f':
                gen = 'FEM'
            elif g == 'm':
                gen = 'MAS'
            elif g in ['pl.','pl']:
                gen = 'PLU'
            else:
                gen = None
    else:
        gen = None
    definition = spl[1]
    wort = deutsch

    return wort, theme, definition, gen





