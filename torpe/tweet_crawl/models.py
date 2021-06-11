import datetime
from .twapi import searchTweets
from django.db import models
from django.utils import timezone

class Querie(models.Model):
   
    entry = models.CharField(max_length = 200)
    start_day = models.DateTimeField('data de inicio da consulta')
    end_day = models.DateTimeField('data de termino da consulta')
    executed_on = models.DateTimeField('data de execução da consulta')
    max_itens = models.IntegerField(default=0)
    rank_size = models.IntegerField(default=5)
    #Methods
    def __str__(self):
        return self.entry
    
    def doTweetCrawling(self):
        tweets_list = searchTweets(
            self.entry,
            self.start_day,
            self.end_day,
            self.max_itens)
        return tweets_list
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