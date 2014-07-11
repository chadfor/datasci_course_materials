import json
import re
import sys

def calcFreq(tweet_texts):
    freqDict = {}
    totalTweetWords = 0
    for tweet in tweet_texts:
        for word in tweet:
            totalTweetWords = totalTweetWords + 1
            if word.encode('utf-8') not in freqDict.keys():
                freqDict[word] = 0
            freqDict[word] = freqDict[word] + 1
    return freqDict,totalTweetWords

def calcHist(freqDict,totalTweetWords):
    histDict = {}
    for key in freqDict.keys():
        histDict[key] = float(freqDict[key])/totalTweetWords
    return histDict

def cleanupAllTweets(allTweets):
    cleanTweets = []
    for tweet in allTweets:
        cleanTweets.append(cleanup_tweet(tweet)) 
    return cleanTweets

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

def main():
    tweet_texts = []
    tweet_file = open(sys.argv[1])
    parse_tweets_to_list(tweet_file,tweet_texts)
    cleanTweets = cleanupAllTweets(tweet_texts)
    freqDict,totalTweetWords = calcFreq(cleanTweets)
    histDict = calcHist(freqDict,totalTweetWords)
    printResults(histDict)

def parse_tweets_to_list(tfile,tlist):
    for line in tfile:
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            tlist.append(tweet["text"])

def printResults(histDict):
    for word in histDict.keys():
        print word + ' ' + str(histDict[word])

if __name__ == '__main__':
    main()
