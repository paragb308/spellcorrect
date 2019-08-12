# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 11:22:41 2019

@author: Parag
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def form():
   return render_template('form.html')
    
@app.route('/',methods = ['POST'])
def form_post():
     word_submitted = request.form['text'].lower()
     possible_word = correction(word_submitted)
     return str(possible_word)

if __name__ == "__main__":
    app.run()
    
# =============================================================================
# Spell Correction method 1: Norvig
# =============================================================================

import re
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())

# download big.txt from https://norvig.com/big.txt
WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N


def correction(word):     
    # Org version =================================
    
    "Most probable spelling correction for word."
#    return max(candidates(word), key=P)

#    # v2 : Generating best 3 cases ================
    candidates_set = candidates(word)
    op_list = []
    for i in range(min(len(candidates_set ), 3)):
        op_list.append(max(candidates_set, key=P))
        candidates_set = candidates_set - {op_list[i]}
    return op_list

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# =============================================================================
# Testing
# =============================================================================


def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]
    
# download text file from https://norvig.com/spell-testset1.txt

#spelltest(Testset(open('spell-testset1.txt')), verbose = True)

# =============================================================================
# 
# =============================================================================




