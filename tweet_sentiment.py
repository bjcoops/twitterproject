import matplotlib.pyplot as plt
import tweet_database as tweetdb
   
def main():
    #tweet_file = open(sys.argv[2])
    tweet_file = open("output.txt")
        
    sentiment_dict = tweetdb.getDictionary()

   
    
    results = {} 
    lineindex = 0 #keep index method until tweet table is built - replace with time
 
    #iterate through each tweet
    for line in tweet_file:
        lineindex = lineindex + 1
        count = 0
        score = 0
        words = line.split(" ")
        new_terms = []
        averageSentiment = None
        
        #iterate through words in tweet and determine tweet sentiment
        for word in words:
            #check db if term already has record, use previous sentiment as param, if available
            old_sentiment = tweetdb.checkDictionary(sentiment_dict, word)
            
            #check if new word and store to be added to db later with average tweet sentiment as term sentiment
            if old_sentiment == 0:
                new_terms.append(word)
                continue
                
            sentiment = tweetdb.checkTerm(word, old_sentiment)

            #add sentiment score for later average
            score = score + sentiment
            count = count + 1 #does Python really not have ++?  

        #handle tweets with only new terms
        try:
            averageSentiment = float(score) / count
        except:
            averageSentiment = 0
        
        #assign sentiment values to tweets in results dictionary        
        #results[line] = float(score) / count
        results[lineindex] = averageSentiment
        
        #add new terms to db
        for term in new_terms:
            tweetdb.checkTerm(term,averageSentiment)
        
    #print results.items()    
    
    x = list(results.keys())
    y = list(results.values())
    
    plt.plot(x, y)
    plt.show()
    

if __name__ == '__main__':
    main()
