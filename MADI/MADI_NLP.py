import math
import sys
import os
from operator import itemgetter
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import pickle
import json
import yake
#from LAME.settings import get_file

train = False
BuildTrainingSet = False

testData = '''One gouge (Labeled D1) was found on inner skin of RH Wing Fillet Panel near FS477, RBL110. Gouge D1 located beside Camloc fastener. P/N 377269-1 (Door Assy, Wing Lower Fillet, FS 477 to 513, RH) was identifiable per the stamp on the actual part and IPC Ch. C130-A-53-50-04-00A-941A-A (See Figures 1-2). No NDT was performed. A visual inspection showed no other reportable damage. Blend-out was not accomplished due to deep gouge. Cascade is unable to find a repair for this discrepancy per SRM due to location of the gouge that is beside the fastener. The cause of the damage is unknown but is suspected to be interference between head fastener located on the aircraft where the subject part installed.

Note: As there is an inner and an outer skin, remaining thickness cannot be determined accurately without preliminary blending.

See Figure 3 for damage photographs.
See Figure 4 for damage dimensions.

Suggested Action: Cascade recommends that LM provide the blend limits of the discrepant part if within limits, then NDT HFEC, do the surface finish per SRM and then leave as is. Otherwise, Cascade requests suitable instructions for in-house repair. 
'''

def trainModel(BuildTrainingSet):
    #build training data on testData
    if BuildTrainingSet:
        wordMeta = getWordMeta(testData)
        df = pd.DataFrame(wordMeta)
        df.to_excel('data.xlsx')
        return
    
    #configure df
    x = pd.read_excel((r'data_old\trainingdata.xlsx'))
    x = x.rename(columns={0:'word', 1:'prev', 2:'tag', 3:'toInt', 4:'len', 5:'y'})
    x['prev'] = x['prev'].fillna(0)
    
    y = x['y']
    x = x.drop('y', axis=1)
    meta = x.drop('word', axis=1)

    #train model
    rf_model = RandomForestClassifier(n_estimators=50, random_state=44)
    rf_model.fit(meta, y)
    pickle.dump(rf_model, open('MADI/models/NLPmodel.pickle', "wb"))

def getWordMeta(data):
    #set variables
    nltk.download("stopwords")
    stop_words = set(stopwords.words('english'))
    wordsRAW = data.split()
    words = []
    wordMeta = []
    finWords = []

    #clean words
    for word in wordsRAW:
        if word not in stop_words:
            word = str(word.translate(str.maketrans('','',string.punctuation.replace('-','').replace('/',''))))
            finWords.append(word)
            word = str(word.translate(str.maketrans('','',string.punctuation)))
            words.append(word)

    #encode tags
    posTags = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', 'A']
    le = preprocessing.LabelEncoder()
    encodedTags = le.fit_transform(posTags)
    encodedTagsDict = dict(zip(posTags, encodedTags))

    #get metadata
    prev = 'A'
    nltk.download('punkt')
    for word in words:
        temp = ['', '', False, 0]
        #get prev word
        if len(prev) == 0 : prev = 'Z'
        for letter in prev:
            temp[0] += str(ord(letter))
        temp[0] = math.log10(int(temp[0]))
        #collect tags
        try:
            tag = nltk.pos_tag(nltk.word_tokenize(word))[0][1]
        except:
            tag = 'A'
            pass
        try:
            temp[1] = encodedTagsDict[tag]
        except:
            temp[1] = encodedTagsDict['A']
            pass
        #try to int
        try: 
            int(word.replace('-',''))
            temp[2] = True
        except:
            pass
        #get len
        temp[3] = len(word)
        #push to tuple
        wordMeta.append((word, temp[0], temp[1], temp[2], temp[3]))
        #set prev
        prev = word
    return [wordMeta, finWords]

def getPNs(data):
    #define variables
    PNList = []
    wordMeta = getWordMeta(data)[0]
    finWords = getWordMeta(data)[1]

    #create and clean df
    try:
        x = pd.DataFrame(wordMeta)
        x = x.rename(columns={0:'word', 1:'prev', 2:'tag', 3:'toInt', 4:'len'})
        x['prev'] = x['prev'].fillna(0)
        meta = x.drop('word', axis=1)
        meta = meta.astype(float)

        #predict PN
        model = pickle.load(open("MADI/models/NLPmodel.pickle", "rb"))
        #model = pickle.loads(get_file('data/NLPmodel.pickle').read())
        for i in range(len(x.index)-1):
            if model.predict(meta.iloc[[i]]) == 1:
                #create list
                PNList.append(finWords[i])
        return PNList
    except Exception as e:
        print(f"Exception is: {e}")
        return PNList

def keywords(data):
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    numOfKeywords = 10

    kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, top=numOfKeywords, features=None)
    keywords = kw_extractor.extract_keywords(data)

    keywordList = []
    for kw in keywords:
        keywordList.append(kw[0])
    return keywordList

#if train : trainModel(BuildTrainingSet)