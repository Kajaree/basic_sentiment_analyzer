import os
import sys, os, re, json
import collections
from pprint import pprint
import nltk

def tag_score(previous_tag, token_score):
    if 'int' in previous_tag:
        token_score *= 2.0
        #print token_score
    elif 'dec' in previous_tag:
        token_score /= 2.0
        #print token_score
    elif 'inv' in previous_tag:
        token_score *= -1.0
        #print token_score
    return token_score
            
def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o
        
def tag_sent(postagged_sentences_list):
    return [[tag_sentence(sentence) for sentence in postagged_sentences] for postagged_sentences in postagged_sentences_list]
    
def tag_sentence(sentence):
    dictionary = getDict()
    return (sentence[0], sentence[1], dictionary.get(sentence[0].lower(), "none"))
    
def tag_remove(sentence):
    for i in range(len(sentence)):
        sentence[i] = [s for s in sentence[i] if s[2] is not 'none']
    return sentence
    
    
def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    if sentiment == 'neutral': return 0
    return 0
   
def sentiment_score(review, initial):
    review = tag_sent(review)
    review = tag_remove(review)
    score = initial
    tags = ["positive", "negative"]
    prefix = ["int", "dec", "inv"]
    for sentence in review:
        max = len(sentence)
        if max != 0:
            for i in range(max):
                if i == 0:
                    if sentence[i][2] in tags:
                        score += value_of(sentence[i][2])
                        #print i, score
                        #print i, score
                elif i > 0 and i < max:
                    current_token = sentence[i]
                    previous_token = sentence[i-1]
                    tag = current_token[2]
                    previous_tag = previous_token[2]
                    if tag in tags:
                        token_score = value_of(tag)
                        #print i, token_score
                        if previous_tag in prefix:
                            token_score = tag_score(previous_tag, token_score)
                            #print i, token_score
                    else:
                        token_score = 0
                    #print score
                    score += token_score 
                    #print i, score
                elif i == max - 1:
                    current_token = sentence[i]
                    tag = current_token[2]
                    if tag in [prefix[1], prefix[2]]:
                        score = tag_score(tag, score)
        #print sentence, score
    return score
    
def getDict():
    path_to_json = 'dicts/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    dictionaries = dict()
    new_words = dict()
    for js in json_files:
        with open(os.path.join(path_to_json, js)) as json_file:
            dictionaries.update(json.load(json_file))
    return dictionaries
    
