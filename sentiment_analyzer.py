import sys, os, re, json, string
import collections
from pprint import pprint
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from sentence_score import sentiment_score
from bigrams import generate_ngram_score


def gen_status(score):
    stat = "none"
    if score == 0:
        stat = "Neutral"
    elif score >0:
        if score <= 3:
            stat = "positive"
        elif score > 3:
            stat = "highly positive"
    elif score < 0:
        if score >= -3:
            stat = "negative"
        elif score < -3:
            stat = "highly negative"
    return stat
    
def pos_tag(sentences):
    pos = [nltk.pos_tag(sentence) for sentence in sentences]
    return pos

def replace_tag(text):
    with open('word_replace.json') as data_file:    
        dict = json.load(data_file)
    pattern = re.compile(r'\b(' + '|'.join(dict.keys()) + r')\b')
    result = pattern.sub(lambda x: dict[x.group()], text)
    return result
    
def processText(tweet):
    # process the tweets

    #Convert to lower case
    #tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    tweet = tweet.replace('AT_USER', '')
    return tweet

def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
    
def repl(matchObj):
   char = matchObj.group(1)
   return "%s%s" % (char, char)
   
def replace_abrev(text):
    with open('abrev.json') as data_file:    
        abrevs = json.load(data_file)
    pattern = re.compile(r'\b(' + '|'.join(abrevs.keys()) + r')\b')
    result = pattern.sub(lambda x: abrevs[x.group()], text.upper())
    return result
    
    
def pos_tag_remove(text):
    pos_tags = ['FW', 'IN', 'NNP', 'NNPS', 'PRP', 'PRPS', 'UH', 'DT']
    sentences = []
    for i in range(len(text)):
        text[i] = [s for s in text[i] if s[1] not in pos_tags]
    return text

def emoji_replace(text):
    with open('emoji.json') as data_file:    
        emojis = json.load(data_file)
    emt = dict()
    for emoji in emojis:
        for i in range(len(emoji)):
            emt.update({emoji[0]: emoji[1]})
    pattern = re.compile('|'.join( re.escape(emo) for emo in emt))
    result = pattern.sub(lambda x: emt[x.group()], text)
    return result
    
def split(text):
    nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
    nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
    text = emoji_replace(text)
    sentences = nltk_splitter.tokenize(text)
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    table = string.maketrans("","")
    try:
        tokenized_sentences = [nltk_tokenizer.tokenize(sent.translate(remove_punctuation_map)) for sent in sentences]
    except:
        tokenized_sentences = [nltk_tokenizer.tokenize(sent.translate(table, string.punctuation)) for sent in sentences]
    return tokenized_sentences
        
'''def change_verb(text):
    tags = ["VBD", "VBN", "VBG", "VBZ"]
    t = []
    for i in range(len(text)):
        for s in text[i]:
            print s
            if s[1] not in tags:
                t.append(s)
            elif s[0] in ["was", "is"]:
                t.append(s)
            elif s[1] in tags:
                new_tag = nltk.stem.WordNetLemmatizer().lemmatize(s[0], 'v')
                item = (new_tag, "VBP")
                t.append(item)
    return t'''

def assign_score(tweet):
    tweet = replace_abrev(tweet)
    tweet = tweet.lower()
    tweet = tweet.replace("..", ". ")
    tweet = tweet.replace('-', " ")
    tweet = replace_tag(tweet)
    tweet = processText(tweet)
    tweet = replaceTwoOrMore(tweet)
    splitted_sentences = split(tweet)
    #print splitted_sentences
    ngram_score = generate_ngram_score(splitted_sentences)
    #print ngram_score
    pos_tag_sents = pos_tag(splitted_sentences)
    #print pos_tag_sents
    filtered_sentences = pos_tag_remove(pos_tag_sents)
    #print filtered_sentences
    score = sentiment_score(filtered_sentences, ngram_score)
    #print score
    return score
        
if __name__ == "__main__":
    text = raw_input("Enter the text: ")
    print text
    
    text = replace_abrev(text)
    text = text.lower()
    text = text.replace("..", ". ")
    text = text.replace('-', " ")
    text = replace_tag(text)
    text = processText(text)
    #print text
    text = replaceTwoOrMore(text)
    #print text
    splitted_sentences = split(text)
    print splitted_sentences
    ngram_score = generate_ngram_score(splitted_sentences)
    print ngram_score
    pos_tag_sents = pos_tag(splitted_sentences)
    pprint(pos_tag_sents)
    filtered_sentences = pos_tag_remove(pos_tag_sents)
    print filtered_sentences
    score = sentiment_score(filtered_sentences, ngram_score)
    print text , "  ", score, "  ", gen_status(score)
    
 