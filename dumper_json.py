#!/usr/bin/env python
# encoding: utf-8
# modified based on the source code at https://gist.github.com/yanofsky/5436496
# filter the geotagged tweets only 
# Contact: songgaogeo@gmail.com

import tweepy #https://github.com/tweepy/tweepy
import json
import sys
import os

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)		
		#save most recent tweets
		alltweets.extend(new_tweets)
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		print ("...%s tweets downloaded so far" % (len(alltweets)))
		
  #in order to create a json array object
	with open(screen_name+'_tweets.json', mode='w') as f:
		f.write('[')
	##only export the geotagged tweets
	for tweet in alltweets:
		if(tweet.geo):
			with open(screen_name+'_tweets.json', mode='a', encoding='utf-8') as f:
				jsonobj={"id_str":tweet.id_str,"created_at":str(tweet.created_at),"geo":tweet.geo, "text":tweet.text}
				json.dump(jsonobj,f)
				f.write(',')
	#remove the last character
	with open(screen_name+'_tweets.json', 'rb+') as filehandle:
		filehandle.seek(-1, os.SEEK_END)
		filehandle.truncate()
  #in order to create a json array object
	with open(screen_name+'_tweets.json', mode='a') as f:
		f.write(']')
	f.close()
	
if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("gissong")
