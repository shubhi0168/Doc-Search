import re
import os
import glob
import json
import math
import nltk
import pandas as pd
import pathlib
import numpy as np # linear algebra
from itertools import combinations 
from collections import defaultdict 
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from scipy import spatial
from nltk.metrics import edit_distance
from collections import defaultdict 
from .Lesk import Lesk

class WordNet:
     
    def __init__(self): 
        self.STOP_WORDS = nltk.corpus.stopwords.words()
        
    def tokenize(self, q1, q2):
        return word_tokenize(q1), word_tokenize(q2)


    def posTag(self, q1, q2):
        return nltk.pos_tag(q1), nltk.pos_tag(q2)


    def stemmer(self, tag_q1, tag_q2):
        stem_q1 = []
        stem_q2 = []

        for token in tag_q1:
            stem_q1.append(stem(token))

        for token in tag_q2:
            stem_q2.append(stem(token))

        return stem_q1, stem_q2
    
    def path(self, set1, set2):
        return wn.path_similarity(set1, set2)


    def wup(self, set1, set2):
        return wn.wup_similarity(set1, set2)


    def edit(self, word1, word2):
        if float(edit_distance(word1, word2)) == 0.0:
            return 0.0
        return 1.0 / float(edit_distance(word1, word2))

    def computePath(self, q1, q2):

        R = np.zeros((len(q1), len(q2)))

        for i in range(len(q1)):
            for j in range(len(q2)):
                if q1[i][1] == None or q2[j][1] == None:
                    sim = self.edit(q1[i][0], q2[j][0])
                else:
                    sim = self.path(wn.synset(q1[i][1]), wn.synset(q2[j][1]))

                if sim == None:
                    sim = self.edit(q1[i][0], q2[j][0])

                R[i, j] = sim

        # print R

        return R

    def computeWup(self, q1, q2):
        
        R = np.zeros((len(q1), len(q2)))

        for i in range(len(q1)):
            for j in range(len(q2)):
                if q1[i][1] == None or q2[j][1] == None:
                    sim = self.edit(q1[i][0], q2[j][0])
                else:
                    sim = self.wup(wn.synset(q1[i][1]), wn.synset(q2[j][1]))

                if sim == None:
                    sim = self.edit(q1[i][0], q2[j][0])

                R[i, j] = sim

        # print R

        return R

    def overallSim(self, q1, q2, R):

        sum_X = 0.0
        sum_Y = 0.0

        for i in range(len(q1)):
            max_i = 0.0
            for j in range(len(q2)):
                if R[i, j] > max_i:
                    max_i = R[i, j]
            sum_X += max_i

        for i in range(len(q1)):
            max_j = 0.0
            for j in range(len(q2)):
                if R[i, j] > max_j:
                    max_j = R[i, j]
            sum_Y += max_j

        if (float(len(q1)) + float(len(q2))) == 0.0:
            return 0.0

        overall = (sum_X + sum_Y) / (2 * (float(len(q1)) + float(len(q2))))

        return overall

    def clean_sentence(self, val):
        "remove chars that are not letters or numbers, downcase, then remove stop words"
        regex = re.compile('([^\s\w]|_)+')
        sentence = regex.sub('', val).lower()
        sentence = sentence.split(" ")

        for word in list(sentence):
            if word in self.STOP_WORDS:
                sentence.remove(word)

        sentence = " ".join(sentence)
        return sentence
    
    def semanticSimilarity(self, q1, q2):
        tokens_q1, tokens_q2 = self.tokenize(q1, q2)
        # stem_q1, stem_q2 = stemmer(tokens_q1, tokens_q2)
        tag_q1, tag_q2 = self.posTag(tokens_q1, tokens_q2)

        sentence = []
        for i, word in enumerate(tag_q1):
            if 'NN' in word[1] or 'JJ' in word[1] or 'VB' in word[1]:
                sentence.append(word[0])

        sense1 = Lesk(sentence)
        sentence1Means = []
        for word in sentence:
            sentence1Means.append(sense1.lesk(word, sentence))

        sentence = []
        for i, word in enumerate(tag_q2):
            if 'NN' in word[1] or 'JJ' in word[1] or 'VB' in word[1]:
                sentence.append(word[0])

        sense2 = Lesk(sentence)
        sentence2Means = []
        for word in sentence:
            sentence2Means.append(sense2.lesk(word, sentence))
        # for i, word in enumerate(sentence1Means):
        #     print sentence1Means[i][0], sentence2Means[i][0]

        R1 = self.computePath(sentence1Means, sentence2Means)
        R2 = self.computeWup(sentence1Means, sentence2Means)

        R = (R1 + R2) / 2

        # print R

        return self.overallSim(sentence1Means, sentence2Means, R)