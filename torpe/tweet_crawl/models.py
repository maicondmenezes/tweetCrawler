from .twapi import searchTweets
from django.db import models
from django.utils import timezone

class Querie(models.Model):
   
    entry = models.CharField(max_length = 200)
    start_day = models.DateField('data de inicio da consulta')
    end_day = models.DateField('data de termino da consulta')
    executed_on = models.DateField('data de execução da consulta', default=timezone.now())
    max_itens = models.IntegerField(default=0)
    rank_size = models.IntegerField(default=5)
    crawled_tweets = models.IntegerField(default=0)
    #Methods
    def __str__(self):
        return self.entry    

    def doTweetCrawling(self):  
        tweets_list = searchTweets(
            self.entry,
            self.start_day,
            self.end_day,
            10
        )
        tweets_amount = len(tweets_list)
        if (tweets_amount !=0):
            for tweet in tweets_list:
                new_tweet = Tweet(
                    id_str = tweet.id_str,
                    created_at = tweet.created_at,
                    created_by = tweet.author.id_str,
                    querie = self,
                    text = tweet.text
                )                    
                new_tweet.save()
            tweets_amount = len(tweets_list)
            self.crawled_tweets = tweets_amount
            self.save()
        return tweets_amount
'''
    def rankingTweetsTerms(self, tweets_list):
        bag_of_nouns = twapi.extractTweetsNouns(tweets_list)
        ranked_terms = twapi.rankingItems(bag_of_nouns)
        return ranked_terms
    
    def rankingTweetsEntities(self, tweets_list):
        bag_of_entities = twapi.identifyEntities(tweets_list)
        ranked_entities = twapi.rankingItems(bag_of_entities)
        return ranked_entities
    
    def plotPopulars(self, ranked_list, plot_title):
        plot = twapi.plotRanking(
            ranked_list, 
            self.rank_size, 
            plot_title
        )
        return plot
    
    def doFullAnalisys(self):
        return processFullWorkflow(
            self.querie_entry,
            self.start_day,
            self.end_day,
            self.rank_size
        )
      
'''

class Tweet(models.Model):
    id_str = models.CharField(max_length = 20)
    created_at = models.DateTimeField('data de criação do tweet')
    created_by = models.CharField(max_length = 10)
    querie = models.ForeignKey(Querie, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    
    #Methods
    def __str__(self):
        return self.text