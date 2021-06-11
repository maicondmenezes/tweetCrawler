from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.utils import timezone as tz
from .models import Querie, Tweet
from .forms import QuerieForm
from django.template import loader

def index(request):
    form = QuerieForm()
    if ( request.method == 'POST'):
        form = QuerieForm(request.POST)
        if(form.is_valid()):
            querie_entry = form.cleaned_data['entry']
            querie_start_day = form.cleaned_data['start_day']
            querie_end_day = form.cleaned_data['end_day']
            querie_rank_size = form.cleaned_data['rank_size']
            new_querie = Querie(
                entry = querie_entry, 
                start_day = querie_start_day, 
                end_day = querie_end_day, 
                rank_size = querie_rank_size, 
                executed_on = tz.now()
            )
            new_querie.save()
            tweets = new_querie.doTweetCrawling()
            if (tweets):
                for tweet in tweets:
                    new_tweet = Tweet(
                        id_str = tweet.id_str,
                        created_at = tweet.created_at,
                        created_by = tweet.author.id_str,
                        querie = new_querie.id,
                        text = tweet.text
                    )                    
                    new_tweet.save()
            return redirect('tweet_crawl:querie_list')
    elif(request.method == 'GET'):
            
        return render(request, 'tweet_crawl/index.html', {'form':form})
    
def querie_list(request):
    queries =  Querie.objects.order_by('-executed_on')
    return render(request, 'tweet_crawl/querie_list.html', {'queries': queries})
    
def tweet_list(request, querie_id):
    querie = get_object_or_404(Querie, pk=querie_id)
    total = len(get_list_or_404(Tweet, querie=querie_id))
    return render(request, 'tweet_crawl/tweet_list.html', {'querie': querie, 'total': total })
    
def analisys(request, querie_id):
    
    response = 'analisys on %s querie'
    
    return HttpResponse(response % querie_id)

def search(request, querie_id):
    
    response = 'search on %s querie'
    
    return HttpResponse(response % querie_id)

    
def tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, 'tweet_crawl/tweet.html', {'tweet': tweet})