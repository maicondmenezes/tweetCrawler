# -*- coding: utf-8 -*-
#@title Biblioteca de Funções
def login_Twitter(chave_consumidor, segredo_consumidor, token_acesso, token_acesso_segredo):

#gerando objeto de autenticação
  autenticacao = tw.OAuthHandler(chave_consumidor, segredo_consumidor)
#gerando tokens
  autenticacao.set_access_token(token_acesso, token_acesso_segredo)
#Conectando ao twitter
  return tw.API(autenticacao, wait_on_rate_limit=True)

def search_tweets(twitter, term, startDay, finalDay, maxItens):
  tweets = tw.Cursor(twitter.search,
              q=term,
              lang='pt',
              since=startDay,
              until=finalDay).items(maxItens)
  tweetsList = [tweet.text for tweet in tweets]
  return tweetsList
   
def count_nouns_occurrencie(tweets):
  #deixa o texto todo em mundo e particiona ele em lista de palavras
  words_in_tweet = [tweet.lower().split() for tweet in tweets]
  listNouns = ['NOUN']
  nouns_in_tweet = []
  #elimina pontuações e extrai apenas os substantivos
  for tweet in words_in_tweet:
    doc = sp(str(tweet))
    tweet_no_punct = [ token.orth_ for token in doc if not token.is_punct and token.pos_ in listNouns]
    nouns_in_tweet.append(tweet_no_punct)
  #Contar ocorrências
  all_words_no_punct = list(itertools.chain(*nouns_in_tweet))
  #Create counter
  counts_nouns = collections.Counter(all_words_no_punct)
  return counts_nouns

def plot_popular_words(wordsList, itensAmount, title):
  popular_words = pd.DataFrame(wordsList.most_common(itensAmount), columns=['words', 'frequency'])
  fig, ax = plt.subplots(figsize=(8, 8))
  # Plot horizontal bar graph
  popular_words.sort_values(by='frequency').plot.barh(x='words',
                      y='frequency',
                      ax=ax,
                      color="purple")
  ax.set_title(title)
  plt.show()

def processTweetQuerie(term, startDay, finalDay, podium):
  twitterConn = login_Twitter(API_KEY, API_SECRET_KEY, token_acesso, token_acesso_segredo)
  tweetsList = search_tweets(twitterConn, term, startDay, finalDay, 2000)
  title = (f'Pesquisa de Tweets por Termos\n'
         f'Termos usados: {term}\n'
         f'Data de início: {startDay} | Data final: {finalDay}\n'
         f'{len(tweetsList)} tweets foram coletados\n'
         f'As {podium} mais usadas no período')
  wordsList = count_nouns_occurrencie(tweetsList)
  plot_popular_words(wordsList, podium, title)

API_KEY = 'BP7tNDh2UPbELpR1sQyiRtY6G'
API_SECRET_KEY = 'XIjfoFhscRr4LqU7sheOYZ6DCOQXtBSZF1AEtaGGbrfVYndi20'
token_acesso = '129916291-pUvGqrqwofqVHsNgvRIg7UkWR3yQW4Bdn54h5oHW'
token_acesso_segredo = 'SzOnefG2Ss7at73XxFKmDYkJ4mr0bd5WHbWsn2PnWiHum'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAM0iQQEAAAAAZk1UJWFH97BC%2FlG8gJuHyAVe40c%3DK0kchtFbdTtVeG6Di8PvNYJuRQ6wwRiVkkfUQv11sCt3JCaA1w'
