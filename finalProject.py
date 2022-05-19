import re
import random as rd
import math


def filteringDataset(filename):
    file=open(r"C:\Users\omara\Desktop\Health-News-Tweets DATASET\Health-Tweets\{}".format(filename)+".txt",'r', encoding="utf8") # encoding="utf8" -->without this we get <UnicodeDecodeError> 
    tweets=list(file)
    #list_of_tweets=[]
    
    for i in range(len(tweets)):
        
        
        #Removing Tweets ID and Timestamps 
        tweets[i]=tweets[i][50:]
        
        
        #Removing URLs 
        #(http\w?.+)
        #(\w{4}\:\/\/\w{3}\.\w{2}.+)
        tweets[i]=re.sub(r'(http\w?.+)','', tweets[i])
        
        
        #Remove any word with symbol (@) 
        tweets[i]=re.sub(r'(@\w[A-z0-9]+)', '' ,tweets[i])
        
        
        #Removing Punctuations
        tweets[i]=re.sub(r'[^\w\s]','', tweets[i]) # [^\w\s] search individual for anything not \s (space) and not \w (alphanumeric)
        #tweets[i]=tweets[i].translate(str.maketrans('','',string.punctuation)) # (string.punctuation) containsAllSymbols --> [ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ]
        
        
        #convert all words to lowerCase
        tweets[i]=tweets[i].lower()
        
        #break when space exists and insert in new list
        #list_of_tweets.append(tweets[i].split())
        tweets[i]=tweets[i].split()
    
    #print(tweets[0])
    file.close()
    return tweets
  
def calculateDistance(tweet1, tweet2):

    # get the intersection
    intersection = set(tweet1).intersection(tweet2)

    # get the union
    union = set(tweet1).union(tweet2)

    # return the jaccard distance
    return 1 - (len(intersection) / len(union))

def getRandomPoints(centroids,k):
    size = 0 # number of centroids
    used = dict() # dict to check if the centroid already exists or not
    flag = True
    
    # to get random centroid
    while (flag):
        if size >= k:
            flag = False
        else: 
            idx = rd.randint(0, len(tweets) - 1)
            if idx not in used:
                size += 1
                used[idx] = True
                centroids.append(tweets[idx])
        
    return centroids

def compute_SSE(clusters):

    sse = 0
    for c in range(len(clusters)):
        for t in range(len(clusters[c])):
            sse +=(clusters[c][t][1] **2)

    return sse



def assign_cluster(tweets, centroids):
    clusters = dict()
    for t in range(len(tweets)):
        
        # dist=list()
        min_dis=math.inf
        cluster_id = -1 # initial value
        
        for c in range(len(centroids)): # will iterate on all centroids --> compare tweet with each centroid
            
            dis = calculateDistance(centroids[c], tweets[t]) # distance will be less than inf for sure
            if centroids[c] == tweets[t]:
                cluster_id = c
                min_dis = 0
                break #----> if error is here then remove break statements
            
            if dis < min_dis:
                cluster_id = c
                min_dis = dis
            # dist.append(dis)
            
            
        if min_dis == 1: # tweet and centroid are completely different then put it in any cluster
            cluster_id = rd.randint(0, len(centroids) - 1)
        
        
        clusters.setdefault(cluster_id, []).append([tweets[t]])    # if cluster_id doesnot exist then put [] and append [tweets[t]] in it
        # add the tweet distance to compute sse in the end
        last_tweet_id = len(clusters.setdefault(cluster_id, [])) - 1
        clusters.setdefault(cluster_id, [])[last_tweet_id].append(min_dis)
        
        
    return clusters

def update_centroids(clusters):

    centroids = []
    for key in range(len(clusters)):
        min_dis_sum = math.inf
        idx = -1
    
        
        for x in range(len(clusters[key])):
            total = 0
            for y in range(len(clusters[key])):
                if x != y:
                    dis = calculateDistance(clusters[key][x][0], clusters[key][y][0])
                    total += dis
                    
            # select the tweet with the minimum distances sum as the centroid for the cluster
            if total < min_dis_sum:
                min_dis_sum = total
                idx = x 
                
        centroids.append(clusters[key][idx][0])
    return centroids

def k_means(tweets, k=3, maxit=30):
    currentCentroids = []
    
    getRandomPoints(currentCentroids, k)
    
    
    previousCentroids = []
    
    for i in range(maxit):
        clusters = assign_cluster(tweets, currentCentroids)
        previousCentroids = currentCentroids
        currentCentroids = update_centroids(clusters)
        
        check = False # will break when len(previousCentroids) == len(currentCentroids) clusters don't change
        if len(previousCentroids) != len(currentCentroids):
            check = True
        
        for c in range(len(currentCentroids)):
            if currentCentroids[c] != previousCentroids[c]:  
                check = True
                
        if check == False:
            break

    sse = compute_SSE(clusters)
    return clusters, sse

############### MAIN #############


filename=input("please enter file name: ")
k=int(input("please enter number of clusters: "))
print()
tweets = filteringDataset(filename)

for e in range(5): ## default number of experiments to be performed
    print("for experiment no. " + str((e + 1)) + "  k = " + str(k))

    clusters, error = k_means(tweets, k)
    
    for c in range(len(clusters)):
       print(str(c+1) + ": ", str(len(clusters[c])) + " tweets")

    print("SSE : " + str(error))
    print('\n')
    print("*"*5)
    # k = k + 1


