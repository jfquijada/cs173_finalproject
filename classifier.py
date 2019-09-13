import math

#opens and cleans neutral words
def neutralWords():
    import re
    file = open("neutralWords.txt", 'r')
    text = file.read().lower()
    file.close()
    text = re.sub('[^a-z\n]+', " ", text) # replaces not lowercase letter, spaces, apostrophes with space
    words = list(text.split('\n'))
    return words

#takes user review file and cleans it up
def cleanUpUserReview(path):
    import re
    file = open(path, 'r')
    text = file.read().lower()
    file.close()
    text = re.sub('[^a-z\ \'\n]+', " ", text)
    words = list(text.split('\n'))
    return words

#reads training sets, cleans up words
def cleanUpWords(path):
    import re
    file = open(path, 'r')
    text = file.read().lower()
    file.close()
    text = re.sub('[^a-z\ \']+', " ", text) #replaces unnecessary characters
    words = list(text.split())
    return words

#creates the likelihood of each words from the training data
def getProbability(words):
    occurences = {} #stores likelihood of words
    commonWords = neutralWords()
    #calculates occurence of each word
    for w in words:
        if w not in commonWords:
            if w in occurences: #if word in list, add to count
                occurences[w] += 1
            else:
                occurences[w] = 1 #else, add to list

    totalWords = 0 #count for total words
    for w in occurences:
        totalWords = totalWords + occurences[w]

    #probability = count(currWord)/count(allwords)
    for w in occurences:
        occurences[w] = float(occurences[w]) / totalWords;

    return occurences

#This function calculates the posteriors to judge whether sentence is positive
def isPositive(sentences, pos, neg):

    #Split sentence by words
    words = sentences.split(' ')

    pos_prob = 0
    neg_prob = 0

    #This function calculates the posteriors for positive and negative likelihood
    for w in words:
        if w in pos:
            pos_prob += math.log(pos[w]) #gives higher probability
        if w not in pos and w in neg:
            pos_prob += math.log(0.000000000000000000001) #lower probability
        if w in neg:
            neg_prob += math.log(neg[w])
        if w not in neg and w in pos:
            neg_prob += math.log(0.000000000000000000001)

    return pos_prob > neg_prob

def countAllReviews(path, pos, neg):
    count = 0
    for sentences in path:
        if isPositive(sentences, pos, neg):
            count += 1
    print (str(count) + " positive reviews " + "out of: " + (str(len(path) - 1)) + " total reviews ")
    print (str((len(path) - 1)  - count) + " negative reviews " + "out of: " + (str(len(path) - 1)) + " total reviews \n")

#This function calculates overall accuracy
def printAnalysis(wordList, pos, neg):
    #For each review, judge whether it's positive
    count = 0
    for sentences in wordList:
        if isPositive(sentences, pos, neg):
            print ("review is POSITIVE")
            count += 1 #accumulates if its positive
        else:
            print ("review is NEGATIVE")

    # print str(count) + " out of " + str(len(wordList)) + " reviews were classified as positive sentiments."

    return float(count) / len(wordList)

###################################
# ------------ MAIN ---------------
###################################

print ("\n...LOADING SENTIMENT ANALYSIS...")

# read training set, clean up words
posWords = cleanUpWords("train-pos.txt")
negWords = cleanUpWords("train-neg.txt")

# getting probabilities of words
posLikelihood = getProbability(posWords)
negLikelihood = getProbability(negWords)

print ("\n" + "(Enter 'q' to exit)")

while True:

    # get test review from user
    takeInput = input("Write your review: ")
    if takeInput == 'q':
        break
    userFile = open("reviewInput.txt", 'w') #overwrite file
    userFile.write(takeInput)
    userFile.close()
    allReviews = open("allReviews.txt", 'a')
    allReviews.write(takeInput + "\n")
    allReviews.close()
    userReview = cleanUpUserReview("reviewInput.txt")
    allReviews = cleanUpUserReview("allReviews.txt")

    # CALCULATING SENTIMENT ANALYSIS FOR POSITIVE AND NEGATIVE TRAINING SET
    printAnalysis(userReview, posLikelihood, negLikelihood)
    countAllReviews(allReviews, posLikelihood, negLikelihood)
