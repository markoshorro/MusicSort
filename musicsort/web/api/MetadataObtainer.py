#!/usr/bin/env python

import os, sys
import requests
import json
import urllib
from subprocess import call

class MetadataSpotify:

	def get_metadata(self, track, artist, imgPath):
		artistList = [] 
		url = "https://api.spotify.com/v1/search?q=" + track + " artist:" + artist + "&type=track&limit=1"
		response = requests.get(url)

		if response.status_code == 200:
			results = response.json()
			if results['tracks']['total'] >= 1:
				imgURL = results['tracks']['items'][0]['album']['images'][1]['url']
				albumType = results['tracks']['items'][0]['album']['album_type']
				albumName = results['tracks']['items'][0]['album']['name']
				for i in range(0, len(results['tracks']['items'][0]['artists'])):
					artistList.append(results['tracks']['items'][0]['artists'][i]['name'])
				explicit = results['tracks']['items'][0]['explicit']
				track_number = results['tracks']['items'][0]['track_number']
				urllib.urlretrieve(imgURL, os.path.join(imgPath, track + " - " + artist + ".jpg"))
				return imgURL ,albumType ,albumName ,artistList ,explicit ,track_number
			else:
				# print "API Spotify: No existen coincidencias para \"" + track + "\" de \"" + artist + "\"."
				return None
		else:
			print "API Spotify: Error code %s" % response.status_code
