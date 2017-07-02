#!/usr/bin/env python3
# coding: utf-8

import sys
import getpass
from mastodon import Mastodon

mastodonSecretsLoc = "mastodon.secret"

def setup():
	print("------------------")
	print("  MASTODON SETUP  ")
	print("------------------\n")

	print("To connect to Mastodon I need some informations.")

	mastodonWorks = False

	while not mastodonWorks:
		print("\n")
		mastodonURL      = "https://" + input("Your Mastodon instance URL: https://")
		mastodonEMail    =              input("      Your Mastodon e-mail: ")
		mastodonPassword =    getpass.getpass("    Your Mastodon password: ")

		print("\nOkay, let's try to connect to Mastodon!\n")

		try:
			Mastodon.create_app(
				'MastoTwitter',
				scopes       = ['read', 'write'],
				api_base_url = mastodonURL,
				to_file      = 'mastodon_client.secret'
			)
		except Exception as error:
			print("Cannot create a Mastodon app: " + error)
			sys.exit(1)


		try:
			api = Mastodon(
				client_id    = 'mastodon_client.secret',
				api_base_url = mastodonURL
			)
			api.log_in(
				username = mastodonEMail,
				password = mastodonPassword,
				to_file  = 'mastodon_user.secret',
				scopes   = ["read", "write"]
			)
		except Exception as error:
			print("You made a mistake, theses informations didn't worked...\nLet's start again!")
			print(error)

		else:
			mastodonWorks = True

	print("Alright, that worked!")

	mastodonSecrets = open(mastodonSecretsLoc, "w")

	mastodonSecrets.write(mastodonURL)

	mastodonSecrets.close()

	print("Theses keys are now saved inside " + mastodonSecretsLoc + ", please keep it secret!")



def connect():

	try:
		mastodonSecrets = open(mastodonSecretsLoc, "r")
	except:
		print("It looks like " + mastodonSecretsLoc + " file isn't here. You need to setup Mastodon first:")

		setup()
		connect()
	else:

		mastodonURL = mastodonSecrets.readline()
		mastodonSecrets.close()

		try:
			api = Mastodon(
				client_id        = "mastodon_client.secret",
				access_token     = "mastodon_user.secret",
				api_base_url     = mastodonURL,
				ratelimit_method = "pace",
			)
		except Exception as error:
			print("There was an error: ")
			print(error)
			print("Let's try again:")

			connect()

		else:
			print(" > Connected to Mastodon!")
			return api
