
#### Naive Bayes classifier model
from numpy import genfromtxt
import xlrd
import pandas as pd
import nltk
import numpy as np
import openpyxl as px
from nltk import sent_tokenize, word_tokenize, pos_tag

train = pd.read_csv("File",delimiter='\t')


list(train)

## Remove duplicate values
#train['duplicate'] = train.duplicated()
import pandas as pd
train = train.drop_duplicates(subset=['comments'], keep=False)
train = train.reset_index()
del train['index']


### Convert upper to lower characters
for i in range(len(train.index)):
    a = train.comments[i]
    train['comments'][i] = a.lower()


### word_tokenize
train['word_tokenize'] = [[]] * len(train.index)

for i in range(len(train.index)):
    train['word_tokenize'][i] = word_tokenize(train['comments'][i])
    

###Removing punctuation
import string
punct = list(string.punctuation)
punct.append("''")
punct.append(":")
punct.append("...")
punct.append("@")
#sent = '''He said,"that's it."'''

def remove_puct(sent):
    train['word_tokenize_p'] = len(train.index)
    for j in range(len(train.index)):
        a =[i for i in sent[j] if i not in punct]
        train['word_tokenize_p'][j] = a

remove_puct(train['word_tokenize'])

#del train['remove_puct']


### pos tagging
train['pos_tag'] =[[]] * len(train.index)
for i in range(len(train.index)):
    train['pos_tag'][i] = pos_tag(train['word_tokenize_p'][i])
    
#len(train.index)

### Creating pos_tag of like words
train['high_pos'] = [[]] * len(train.index)
def postag(keyword,myda):
    
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            b = tagged[pos]
            train['high_pos'][i] =  b[1]
        else:
            train['high_pos'][i] = train['high_pos'][i]

words = ['high','higher','highest']
for word in words:
    postag(word,train['word_tokenize_p'])
         
### Target of like word
train['Targetword_high'] = [[]] * len(train.index)   

for i in range(len(train.index)):
    if train['high_pos'][i] == "JJ" or train['high_pos'][i] == "JJR" or train['high_pos'][i] == "JJS":
        train['Targetword_high'][i] = "positive"
    else:
        train['Targetword_high'][i] = "Neutral"


### Selecting before n-1 words
train['n_1'] =[[]] * len(train.index)
def n_1_keyword(keyword,myda):
    
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            b = tagged[pos - 1]
            train['n_1'][i] =  b[0]

            

### Selecting before n-2 words
def n_2_keyword(keyword,myda):
    train['n_2'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if  (pos - 2) < 0:
                train['n_2'][i] = ''
            else:
                b = tagged[pos - 2]
                train['n_2'][i] =  b[0]

### Selecting before n-3 words
def n_3_keyword(keyword,myda):
    train['n_3'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            #b = tagged[pos - 3]
            if  (pos - 3) < 0:
                train['n_3'][i] = ''
            else:
                b = tagged[pos - 3]
                train['n_3'][i] =  b[0]

### Selecting before n-1 pos tag words
def n_1_tag(keyword,myda):
    train['n_1_tag'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            b = tagged[pos - 1]
            train['n_1_tag'][i] =  b[1]


### Selecting before n-2 pos tag words
def n_2_tag(keyword,myda):
    train['n_2_tag'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            b = tagged[pos - 2]
            train['n_2_tag'][i] =  b[1]
### Selecting before n-3 pos tag words
def n_3_tag(keyword,myda):
    train['n_3_tag'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if  (pos - 3) < 0:
                train['n_3_tag'][i] = ''
            else:
                b = tagged[pos - 3]
                train['n_3_tag'][i] =  b[1]

### Selecting before p-1 words
def p_1_keyword(keyword,myda):
    train['p_1'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if len(tagged) > pos + 1:
               b = tagged[pos + 1]
               train['p_1'][i] =  b[0]
            else:
                train['p_1'][i] = ''

### Selecting before p-2 words
def p_2_keyword(keyword,myda):
    train['p_2'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if len(tagged) > pos + 2:
               b = tagged[pos + 2]
               train['p_2'][i] =  b[0]
            else:
                train['p_2'][i] = ''
                    
                    

### Selecting before p-3 words
def p_3_keyword(keyword,myda):
    train['p_3'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if len(tagged) > pos + 3:
               b = tagged[pos + 3]
               train['p_3'][i] =  b[0]
            else:
                train['p_3'][i] = ''
                

### Selecting before p-1 pos tag words
def p_1_tag(keyword,myda):
    train['p_1_tag'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if len(tagged) > pos + 1:
               b = tagged[pos + 1]
               train['p_1_tag'][i] =  b[1]
            else:
                train['p_1_tag'][i] = ''
                

### Selecting before p-2 pos tag words
def p_2_tag(keyword,myda):
    train['p_2_tag'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if len(tagged) > pos + 2:
               b = tagged[pos + 2]
               train['p_2_tag'][i] =  b[1]
            else:
                train['p_2_tag'][i] = ''
                
### Selecting before p-3 pos tag words
def p_3_tag(keyword,myda):
    train['p_3_tag'] =[[]] * len(train.index)
    for i in range(len(train.index)):
        if keyword in myda[i]:
            pos = myda[i].index(keyword)
            a = myda[i]
            tagged = pos_tag(a)
            if len(tagged) > pos + 3:
               b = tagged[pos + 3]
               train['p_3_tag'][i] =  b[1]
            else:
                train['p_3_tag'][i] = ''

             

### Pass the data for Pre Processing Train Data

n_1_keyword('high',train['word_tokenize_p'])
n_2_keyword('high',train['word_tokenize_p'])
n_3_keyword('high',train['word_tokenize_p'])
n_1_tag('high',train['word_tokenize_p'])
n_2_tag('high',train['word_tokenize_p'])
n_3_tag('high',train['word_tokenize_p'])
p_1_keyword('high',train['word_tokenize_p'])
p_2_keyword('high',train['word_tokenize_p'])
p_3_keyword('high',train['word_tokenize_p'])
p_1_tag('high',train['word_tokenize_p'])
p_2_tag('high',train['word_tokenize_p'])
p_3_tag('high',train['word_tokenize_p'])














