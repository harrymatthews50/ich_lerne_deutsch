# ich_lerne_deutsch
This is a simple package for building German vocabulary. It imeplements several different exercises for recalling wor ddefinitions, noun genders, plural forms and Partizip 2 of verbs. 
The word lists are completely customisable and editable. I have provided a few already of A1 level nouns verbs and adjectives and adverbs. Much of this is borrowed from [here](https://github.com/patsytau/anki_german_a1_vocab). Thank you Patsy.

## Installation
### Install Ananconda
Install anaconda or miniconda from [here](https://www.anaconda.com/). The rest of the installation and running the app will require you to use either the computer terminal (on Mac/Linux) or the 'Anaconda prompt' on Windows. The Anaconda prompt will have been installed when you installed Anaconda.

### Install ich_lerne_deutsch 
Download the contents of the 'scripts' folder and download the the '.whl' file in 'build/'. In the computer terminal (Mac/Linux) or Anaconda prompt (Windows) type the following
```
conda create -n ich_lerne_deutsch_env python=3.10
```
when prompted type 'y'. Then 

```
conda activate ich_lerne_deutsch_env
conda install pip
pip install wheel
```

```
wheel install /path/to/.whl
```
## Building word lists
### Word lists as csv files
Word lists are expected in tab-delimited '.csv' files. Sprecific columns are expected, depending on the type of word (verb, noun, other). See the example word lists in 'csv_word_lists/'. When making your own word list make sure 1) the column headers remain the same as in the examples 2) you save the file as '.csv' with tab as the column delimiter. 


Word lists can be made in a spreadsheet by hand in [Libre Office](https://www.libreoffice.org/)(this software is free) or [Micrososft Excel](https://www.microsoft.com/en-us/microsoft-365/excel).

### Converting word lists into training batches
The word lists in the .csv files must now be divided into batches for learning. To do this, locate where on your computer is the file from scripts/make_word_batches.p. In the computer terminal or Ananconda prompt type:
```
conda activate ich_lerne_deutsch_env
python "/Users/hmatth5/Documents/Projects/ich_lerne_deutsch/scripts/make_word_batches.py"
```




