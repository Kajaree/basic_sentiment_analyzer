import re, json
from nltk.util import ngrams

def generate_phrases(input_list):
    return (" ").join(input_list)

def generate_unigram_score(sent_list):
    unigram = []
    phrase_list = get_phrases()
    for sent in sent_list:
        for grams in sent:
            unigram.append([grams, phrase_list.get(grams, "None")])
    #print unigram
    return generate_score(unigram)
    
def generate_bigram_score(sent_list):
    bigram = []
    phrase_list = get_phrases()
    for sent in sent_list:
        if len(sent)!= 1:
            bigrams = ngrams(sent, 2)
            for grams in bigrams:
                phrase = generate_phrases(grams)
                bigram.append([phrase, phrase_list.get(phrase, "None")])
    #print bigram
    return generate_score(bigram)

def generate_trigram_score(sent_list):
    trigram = []
    phrase_list = get_phrases()
    for sent in sent_list:
        if len(sent)!= 1:
            bigrams = ngrams(sent, 3)
            for grams in bigrams:
                phrase = generate_phrases(grams)
                trigram.append([phrase, phrase_list.get(phrase, "None")])
    #print trigram
    return generate_score(trigram)
       
def get_phrases():
    with open("phrases_list.json", "r") as outfile:
        phrase_list = json.load(outfile)
    return phrase_list
    
def generate_score(ngrams):
    score = 0
    for ngram in ngrams:
        if ngram[1] is not "None":
            score += ngram[1]
    return score
    
def generate_ngram_score(sent_list):
    return (generate_unigram_score(sent_list) + generate_bigram_score(sent_list) + generate_trigram_score(sent_list))