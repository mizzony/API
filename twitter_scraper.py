from twitter_scraper import get_tweets

i=1
for tweet in get_tweets('imcascongress', pages=5):
	# print(i)
	# print(tweet['time'])
	print(tweet['text'])
	# print(tweet['entries'])
	i += 1