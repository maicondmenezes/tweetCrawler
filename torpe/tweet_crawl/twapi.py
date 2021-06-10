import datetime as dtm
import tweepy as twp
import pandas as pds
import spacy as spc
import itertools as itr 
import collections as clt
import mathplot_lib as plt


#Chaves de acesso api do twitter
API_KEY = 'BP7tNDh2UPbELpR1sQyiRtY6G'
API_SECRET_KEY = 'XIjfoFhscRr4LqU7sheOYZ6DCOQXtBSZF1AEtaGGbrfVYndi20'
access_token = '129916291-pUvGqrqwofqVHsNgvRIg7UkWR3yQW4Bdn54h5oHW'
access_token_secret = 'SzOnefG2Ss7at73XxFKmDYkJ4mr0bd5WHbWsn2PnWiHum'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAM0iQQEAAAAAZk1UJWFH97BC%2FlG8gJuHyAVe40c%3DK0kchtFbdTtVeG6Di8PvNYJuRQ6wwRiVkkfUQv11sCt3JCaA1w'

#Definição de funções auxiliares

def loginTwitter(API_KEY, API_SECRET_KEY):
    
    logger = twp.AppAuthHandler(API_KEY, API_SECRET_KEY)
    return twp.API(logger, wait_on_rate_limit = True)

def searchTweets(terms, start_day=dtm.datetime.now(), end_day=dtm.datetime.now(), max_itens=0):
    
    twitter = loginTwitter(API_KEY, API_SECRET_KEY)
    tweets_list = twp.Cursor(
        twitter.search,
        q = terms,
        lang = 'pt',
        since = start_day,
        until = end_day
    ).items(max_itens)
    
    return tweets_list
    
def rankingItems(items_list):
    bag_of_items = list(itertools.chain(*items_list))
        
    ranked_items = collections.Counter(bag_of_items)
    return ranked_items
        
def extractTweetsNouns(tweets_list):
    
    tweets_texts = [tweet.text for tweet in tweets]
    tweets_texts_words = [tweet_text.lower().split() for tweet_text in tweets_texts]
    POS_type = ['NOUN']
    noun_in_tweets = []
    
    for tweet_words in tweets_texts_words:
        
        doc = sp(str(tweet_words))
        tweet_nouns = [token.orth_ for token in doc if not token.is_punct and token.pos_ in POS_type]
        nouns_in_tweets.append(tweet_nouns)
    return nouns_in_tweets

def identifyTweetsEntities(tweets_list):
    
    tweets_texts = [tweet.text for tweet in tweets]
    tweets_entities = []
    
    return tweets_entities
    
def plotRanking(ranked_list, rank_size=10, title=''):
    ranked_items = pds.DataFrame(ranked_list.most_common(rank_size), columns=['terms', 'ocorrencies'])
    fig, ax = plt.subplots(figsize(8, 8))
    ranked_items.sort_values(by='ocorrencies').plot.barh(
        x='terms', 
        y='ocorrencies', 
        ax=ax, 
        color='purple')
    ax.set_title(title)
    
    return plt
    
def processFullWorkflow(terms, start_day=dtm.now(), end_day=dtm.now(), max_itens=1000):
    
    return 'ok'