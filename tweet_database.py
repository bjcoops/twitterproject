import sqlite3 as lite

#########################################
#                                       #
# Need to look at classes from notebook #
#                                       #
#########################################


class tweet:
 
    def __init__ (self):
        self.text = ""
        self.sentiment = 0
        self.time = None
        self.user = ""     

class tweetbucket: 
    
    def __init__(self):
        self.tweets = ()
        self.averageSentiment = 0.0   
        
    def fillBucket(self, tweet):
        #add tweet to bucket
        self.tweets.append(tweet)
        #update bucket sentiment average
        self.setBucketAverage(tweet.sentiment)
        return self.tweets.count()        

    def findTweet(self, param):
        #look up tweet 
        return "Look up tweet"   
        
    def getBucketAverage(self):
        return self.averageSentiment
        
    def setBucketAverage(self, sentiment):
        oldAverage = (self.tweets.count() - 1) * self.averageSentiment
        newBucketCount = self.tweets.count()
        newAverage = (oldAverage + sentiment) / newBucketCount
        self.averageSentiment = newAverage
        
                    
    averageSentiment = property(getBucketAverage)

#########################################    
        
                
    
def buildDatabase():
    afinnfile = open("AFINN-111.txt")
    scores = [] #init empty list
    for line in afinnfile:
        term, score = line.split("\t") #afinn file is tab delimited
        record = (term.decode('utf-8'), 1, 0, score)
        scores.append(record)
        
        #scores[term] = int(score) #convert score to integer
        
    con = lite.connect('test.db')
    
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Sent_Dict")
        ###### Add user and time to table ######
        cur.execute("CREATE TABLE Sent_Dict(Word TEXT, SeedFlag INT, Occurrences INT, Sentiment REAL)") 
        cur.executemany("INSERT INTO Sent_Dict VALUES(?, ?, ?, ?)", scores)
        cur.execute("SELECT Word, Sentiment FROM Sent_Dict")
        
        results = cur.fetchall()
        return results

def getDictionary():
    con = lite.connect('test.db')
    
    with con:
        results = {} #init dictionary
        cur = con.cursor()
        cur.execute("SELECT Word, Sentiment FROM Sent_Dict")      
        items = cur.fetchall()
                
        for item in items:
            results[item[0].encode('utf-8')] = item[1]
            
        return results            
                                    
                        
def checkDictionary(dictionary, searchterm):
    if searchterm in dictionary:
        return dictionary[searchterm]
    else:
        return 0
    
def checkTerm(term, sentiment):
    con = lite.connect('test.db')
    modTerm = term.decode('utf-8')
    
    with con:
        cur = con.cursor()
    
        cur.execute("SELECT * FROM Sent_Dict WHERE Word=?", (modTerm,))
        data = cur.fetchall()
        
        #check if no match
        if len(data) == 0:
            #build record
            record = (modTerm, 0, 1, sentiment)
            cur.execute("INSERT INTO Sent_Dict VALUES(?, ?, ?, ?)", record)

            #get sentiment from database and return
            result = cur.execute("SELECT Sentiment FROM Sent_Dict WHERE Word=?", (modTerm,))
            return float(result.fetchone()[0])
      
        #check sentiment flag to exclude seed terms
        elif data[0][1] == 0:
            occurrences = data[0][2]
            new_occurrences = occurrences + 1
            old_sentiment = data[0][3]          
            
            #update to new average sentiment
            new_sentiment = ((occurrences * old_sentiment) + sentiment) / new_occurrences
            
            record = (modTerm, 0, 1, new_sentiment)
            
            #update existing word sentiment   
            cur.execute("INSERT INTO Sent_Dict VALUES(?, ?, ?, ?)", record)      

            #get sentiment from database and return
            result = cur.execute("SELECT Sentiment FROM Sent_Dict WHERE Word=?", (modTerm,))
            return float(result.fetchone()[0])
                        
        #word is from seed research dictionary, doesn't need modification
        else:   
            #get sentiment from database and return
            result = cur.execute("SELECT Sentiment FROM Sent_Dict WHERE Word=?", (modTerm,))
            return float(result.fetchone()[0])

print getDictionary()