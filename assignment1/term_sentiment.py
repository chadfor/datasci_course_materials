import json
import re
import sys

scores = {} # sentiment dictionary
tweet_texts = []
drvdSent = {}
tweetSent = {}
drvdSentCnt = {}

def build_drvdSent(tweet_texts,scores):
    # for 'new' words, assume sentiment matches that of the containing tweet
    for tweet in tweet_texts:
        words = cleanup_tweet(tweet)#.split()
        for word in words:
            # only add words not in the provided file
            if word.encode('utf-8') not in scores.keys():
                # add tweet sentiments to dict for efficiency
                if tweet not in tweetSent.keys():
                    tweetSent[tweet] = score_tweet_sent(tweet)
                # init dict to zero for new words
                if word not in drvdSent.keys():
                    drvdSent[word] = float(0)
                    drvdSentCnt[word] = 0
                # accumulate sentiment (normalize later)
                drvdSent[word] = drvdSent[word] + tweetSent[tweet]
                drvdSentCnt[word] = drvdSentCnt[word] + 1
    # post-process 'new' word sentiments to normalize over all tweets
    for word in drvdSent.keys():
        if 0 != drvdSentCnt[word]: 
            drvdSent[word] = drvdSent[word]/drvdSentCnt[word]
        else:
            error('error normalizing sentiment')

# use regex to remove all non-text/space
#  allow hashtag (conditional) for later use
def cleanup_tweet(tweet):
    p = re.compile(r'\b[A-z\']*\b')
    res = p.findall(tweet)
    wordList = []
    for word in res:
        if word != '':
            wordList.append(word)
    return wordList

def get_sent_score(term):
    if term.encode('utf-8') in scores.keys():
        return scores[term]
    else:
        return 0

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse_sent_to_dict(sent_file,scores)
    parse_tweets_to_list(tweet_file,tweet_texts)
    build_drvdSent(tweet_texts,scores)
    printResults()

def parse_sent_to_dict(sfile,sdict):
    for line in sfile:
        term,score = line.split("\t")
        sdict[term] = int(score)

def parse_tweets_to_list(tfile,tlist):
    for line in tfile:
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            tlist.append(tweet["text"])

def printResults():
    for word in drvdSent.keys():
        print word + ' ' + str(drvdSent[word])

def score_tweet_sent(tweet):
    score = 0
    words = cleanup_tweet(tweet)#.split()
    for word in words:
        score = score + get_sent_score(word)
    return score

if __name__ == '__main__':
    main()
