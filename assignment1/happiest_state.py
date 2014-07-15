import json
import re
import sys

def cleanupAllTweets(allTweets):
    cleanTweets = []
    for tweet in allTweets:
        cleanTweets.append(cleanupTweet(tweet)) 
    return cleanTweets

# use regex to remove all non-text/space
#  allow hashtag (conditional) for later use
def cleanupTweet(tweet):
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
    scores = {} # sentiment dictionary
    tweet_texts = []
    tweet_place = []

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = parse_sent_to_dict(sent_file)
    parsed_tweet = parse_tweets(tweet_file)
#    cleanTweets = cleanupAllTweets(parsed_tweet)
    printResults(parsed_tweet)

def parse_sent_to_dict(sfile):
    scores = {}
    for line in sfile:
        term,score = line.split("\t")
        scores[term] = int(score)
    return scores

def parse_tweets(tfile):
    parsed_tweet = []
    for line in tfile:
        tweet = json.loads(line)
        if 'text' and 'place' in tweet.keys() and tweet['place'] != None:
            parsed_tweet.append([tweet["text"],tweet["place"]])
    return parsed_tweet

#def _parse_tweet_state(json_tweet):
#    if 'place' in json_tweet and json_tweet['place']!=null:
#    elif 'user' in json_tweet:

def printResults(parsed_tweet):
    for tweet in parsed_tweet[0:10]:
        print parsed_tweet[0] + '\n\t' + parsed_tweet[1]
    return

def score_tweet_sent(tweet):
    score = 0
    words = cleanup_tweet(tweet)#.split()
    for word in words:
        score = score + get_sent_score(word)
    return score

if __name__ == '__main__':
    main()
