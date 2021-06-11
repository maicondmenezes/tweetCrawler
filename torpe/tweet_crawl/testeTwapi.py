from twapi import searchTweets

querie_entry = 'from:maicondmenezes'
querie_start_day = '2021-06-05'
querie_end_day = '2021-06-10'

tweets = searchTweets(
                        querie_entry, 
                        querie_start_day,
                        querie_end_day,
                        1                        
            )
for tweet in tweets:
    print(str(tweet.id_str)+'\n')  
    print(str(tweet.created_at)+'\n')
    print(str(tweet.author.id_str)+'\n')
    print(str(tweet.text)+'\n')
    
        