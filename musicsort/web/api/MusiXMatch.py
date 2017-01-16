#!/usr/bin/env python

import requests
import json
import urllib
from subprocess import call

class MusiXMatchLyrics:
		
	def get_metadata(self, track, artist):
		apikey= "663a730e8ddf699a897fc859c81bee67"
		url = "http://api.musixmatch.com/ws/1.1/matcher.lyrics.get?q_track=" + track + "&q_artist=" + artist + "&apikey=" + apikey + "&format=json"
		response = requests.get(url)

		if response.status_code == 200:
			results = response.json()
			if results['message']['header']['status_code'] == 404:
				# print "API MusicXMatch: No existen coincidencias para \"" 
				# + track + "\" de \"" + artist + "\"."
				pass
			else:
				return results['message']['body']['lyrics']['lyrics_body']
		else:
			print "API MusicXMatch: Error code %s" % response.status_code
