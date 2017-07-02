#!/usr/bin/env python3
# coding: utf-8

import twitter

twitterSecretsLoc = "twitter.secret"

def setup():
	print("-----------------")
	print("  TWITTER SETUP  ")
	print("-----------------\n")

	print("To connect to Twitter I need some keys. You can get them by creating an app on https://apps.twitter.com.")
	print("Once you have created a Twitter App, we can begin!")

	twitterWorks = False

	while not twitterWorks:
		print("\n")
		twitterConsumerKey    = input("      Consumer Key (API Key): ")
		twitterConsumerSecret = input("Consumer Secret (API Secret): ")
		twitterAccessToken    = input("                Access Token: ")
		twitterAccessSecret   = input("         Access Token Secret: ")

		print("\nOkay, let's try to connect to Twitter!\n")

		try:
			api = twitter.Api(
				consumer_key        = twitterConsumerKey,
				consumer_secret     = twitterConsumerSecret,
				access_token_key    = twitterAccessToken,
				access_token_secret = twitterAccessSecret
			)
			api.VerifyCredentials()

		except:
			twitterWorks = False
			print("You made a mistake, theses keys didn't worked...\nLet's start again!")

		else:
			twitterWorks = True

	print("Alright, that worked!")


	twitterSecrets = open(twitterSecretsLoc, "w")

	twitterSecrets.write(twitterConsumerKey    + "\n")
	twitterSecrets.write(twitterConsumerSecret + "\n")
	twitterSecrets.write(twitterAccessToken    + "\n")
	twitterSecrets.write(twitterAccessSecret         )

	twitterSecrets.close()

	print("Theses keys are now saved inside " + twitterSecretsLoc + ", please keep it secret!")


def connect():

	try:
		twitterSecrets = open(twitterSecretsLoc, "r")
	except:
		print("It looks like " + twitterSecretsLoc + " file isn't here. You need to setup Twitter first:")

		setup()
		connect()
	else:

		keys = twitterSecrets.readlines()
		twitterSecrets.close()

		if len(keys) != 4:
			print("It looks like " + twitterSecretsLoc + " file is corrupted. You need to setup again Twitter:")
			setup()
			connect()
		else:

			try:
				api = twitter.Api(
					consumer_key        = keys[0].rstrip(),
					consumer_secret     = keys[1].rstrip(),
					access_token_key    = keys[2].rstrip(),
					access_token_secret = keys[3].rstrip()
				)
				api.VerifyCredentials()
			except:
				print("The keys inside " + twitterSecretsLoc + " doesn't work. You need to setup again Twitter:")
				setup()
				connect()
			else:
				print(" > Connected to Twitter!")
				return api
