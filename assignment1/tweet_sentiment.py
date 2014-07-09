import json
import re
import sys

scores = {} # sentiment dictionary
tweet_texts = []

# use regex to remove all none text/space
#  allow hashtag (conditional) for later use
def cleanup_tweet(tweet):
    p = re.compile(r'\b[A-z\']*\b')
    res = p.findall(tweet)
    wordList = []
    for word in res:
        if word != '':
            wordList.append(word)
    return wordList
#    return tweet.replace('.','').replace(',','').replace(':','').replace(';','').replace('-','')

def get_sent_score(term):
#    print term
# fix for unicode
#    if term in scores.keys():
    if term.encode('utf-8') in scores.keys():
        return scores[term]
    else:
        return 0

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse_sent_to_dict(sent_file,scores)
#    print_sent()
    parse_tweets_to_list(tweet_file,tweet_texts)
#    print_tweets()
    score_tweets()

def parse_sent_to_dict(sfile,sdict):
    for line in sfile:
        term,score = line.split("\t")
        sdict[term] = int(score)

def print_sent():
    print scores.items()

def parse_tweets_to_list(tfile,tlist):
    for line in tfile:
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            tlist.append(tweet["text"])

def score_tweets():
    for tweet in tweet_texts:
        tw_score = score_sent(tweet)
        str_tw_score = str(tw_score) + '\n'
        if tw_score != 0:
            print tweet
            print tw_score

def print_tweets():
    for tweet in tweet_texts:
        print tweet

def score_sent(tweet):
    score = 0
    words = cleanup_tweet(tweet)#.split()
#    print 'start\n'
    for word in words:
        score = score + get_sent_score(word)
#        print word,score
    return score
    

if __name__ == '__main__':
    main()
