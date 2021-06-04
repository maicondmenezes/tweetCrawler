#@title Biblioteca de funções execute este trecho após o cabeçalho
# -*- coding: utf-8 -*-
def login_Twitter(chave_consumidor, segredo_consumidor, token_acesso, token_acesso_segredo):

#gerando objeto de autenticação
  autenticacao = tw.OAuthHandler(chave_consumidor, segredo_consumidor)
#gerando tokens
  autenticacao.set_access_token(token_acesso, token_acesso_segredo)
#Conectando ao twitter
  return tw.API(autenticacao, wait_on_rate_limit=True)

def search_tweets(twitter, term, startDay, finalDay, maxItens):
  tweets = tw.Cursor(twitter.search,
              q=term,
              lang='pt',
              since=startDay,
              until=finalDay).items(maxItens)

  
  tweetsList = [tweet.text for tweet in tweets]
  return tweetsList

def extract_nouns_list(tweets, out):
  counter = 0
  leitorMAX = int(len(tweets))
  #deixa o texto todo em mundo e particiona ele em lista de palavras
  words_in_tweet = [tweet.lower().split() for tweet in tweets]
  listNouns = ['NOUN']
  nouns_in_tweet = []
  #elimina pontuações e extrai apenas os substantivos
  for tweet in words_in_tweet:
    doc = sp(str(tweet))
    tweet_no_punct = [ token.orth_ for token in doc if not token.is_punct and token.pos_ in listNouns]
    nouns_in_tweet.append(tweet_no_punct)
    counter+=1
    out.update(progress('Extraindo substantivos...', counter, leitorMAX))
  return nouns_in_tweet
  
def count_words_frequency(wordsList):
  bagOfWords = list(itertools.chain(*wordsList))
  #Create counter
  words_frequency = collections.Counter(bagOfWords)
  return words_frequency

def plot_popular_words(wordsList, itensAmount, title):
  popular_words = pd.DataFrame(wordsList.most_common(itensAmount), columns=['words', 'frequency'])
  fig, ax = plt.subplots(figsize=(8, 8))
  # Plot horizontal bar graph
  popular_words.sort_values(by='frequency').plot.barh(x='words',
                      y='frequency',
                      ax=ax,
                      color="purple")
  ax.set_title(title)
  plt.show()

def extract_named_entities(tweetsList, out):
  counter = 0
  leitorMAX = int(len(tweetsList))
  
  namedEntities = []
  for tweet in tweetsList:
    doc = sp(str(tweet))
    tweetEntities = [str(entity) for entity in doc.ents]
    namedEntities.append(tweetEntities)
    counter+=1
    out.update(progress('Identificando entidades...', counter, leitorMAX))
  return namedEntities

def process_tweet_querie(term, startDay, finalDay, podium):
  API_KEY = 'BP7tNDh2UPbELpR1sQyiRtY6G'
  API_SECRET_KEY = 'XIjfoFhscRr4LqU7sheOYZ6DCOQXtBSZF1AEtaGGbrfVYndi20'
  token_acesso = '129916291-pUvGqrqwofqVHsNgvRIg7UkWR3yQW4Bdn54h5oHW'
  token_acesso_segredo = 'SzOnefG2Ss7at73XxFKmDYkJ4mr0bd5WHbWsn2PnWiHum'
  BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAM0iQQEAAAAAZk1UJWFH97BC%2FlG8gJuHyAVe40c%3DK0kchtFbdTtVeG6Di8PvNYJuRQ6wwRiVkkfUQv11sCt3JCaA1w'
  counter = 1
  leitorMAX = 8
  
  out = display(progress('Conectando ao Twitter', counter, leitorMAX), display_id=True)
  outTask = display(progress('...', 0, 1), display_id=True)
  twitterConn = login_Twitter(API_KEY, API_SECRET_KEY, token_acesso, token_acesso_segredo)
  counter+=1
  out.update(progress('Coleta de tweets...', counter, leitorMAX))
  tweetsList = search_tweets(twitterConn, term, startDay, finalDay, 2000)
  title = (f'Pesquisa de Tweets por Termos\n'
         f'Termos usados: {term}\n'
         f'Data de início: {startDay} | Data final: {finalDay}\n'
         f'{len(tweetsList)} tweets foram coletados\n'
         f'As {podium} mais usadas no período')
  counter+=1
  out.update(progress('Extração de Substantivos', counter, leitorMAX))
  nounsInTweets = extract_nouns_list(tweetsList, outTask)
  counter+=1
  out.update(progress('Cálculo de Frequência de Substantivos', counter, leitorMAX))
  nounsFrequency = count_words_frequency(nounsInTweets)
  counter+=1
  out.update(progress('Identificação de entidades', counter, leitorMAX))
  entitiesInTweets = extract_named_entities(tweetsList, outTask)
  counter+=1
  out.update(progress('Cálculo de Frequência de Entidades', counter, leitorMAX))
  entitiesFrequency = count_words_frequency(entitiesInTweets)

  title = (f'Pesquisa de Tweets por Termos\n'
         f'Termos usados: {term}\n'
         f'Data de início: {startDay} | Data final: {finalDay}\n'
         f'{len(tweetsList)} tweets foram coletados\n'
         f'Os {podium} termos mais usadas no período')
  counter+=1
  out.update(progress('Plotagem de frequência de substantivos', counter, leitorMAX))
  plot_popular_words(nounsFrequency, podium, title)

  title = (f'Pesquisa de Tweets por Termos\n'
         f'Termos usados: {term}\n'
         f'Data de início: {startDay} | Data final: {finalDay}\n'
         f'{len(tweetsList)} tweets foram coletados\n'
         f'As {podium} entidades mais mencionadas no período')
  counter+=1
  out.update(progress('Plotagem de frequência de entidades', counter, leitorMAX))
  plot_popular_words(entitiesFrequency, podium, title)

#função para desenhar a barra de progresso
def progress(message, value, max=100):
 progresso = ((value * 100) / max)
return HTML("""
    <span> {message} </span>
      <br>
      <progress
            value='{value}'
            max='{max}',
            style='width: 99%'
      >
       {value}
      </progress>
    <span> {value} | {max} :: {progresso} % :: </span>

      
  """.format(value=value, max=max, progresso=progresso, message=message))
