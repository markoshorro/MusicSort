#!/usr/bin/env python

import os, sys
from MetadataObtainer import MetadataSpotify
from acrcloud.AcrCloudApi import AcrCloudApi
from MusiXMatch import MusiXMatchLyrics
from FileModifier import FileModifier

path = sys.argv[1]
if not (path.endswith("/")):
	path = path + "/"
imgPath = path + "img/"
if not os.path.exists(imgPath):
  os.makedirs(imgPath)
metaD = MetadataSpotify()
acr = AcrCloudApi()
lyrics = MusiXMatchLyrics()
modifier = FileModifier()
resultAcrList = [] 
resultSpotiList = []
files = os.listdir(path) 
i = 0

for x in files:	
	# title, artist, year, genresList
	print "Processing song %d: " % i + x
	i += 1
	resultAcrList = acr.recognize_song(path+x)
	if resultAcrList is not None:
		# imgURL ,albumType ,albumName ,artistList ,explicit ,track_number
		resultSpotiList = metaD.get_metadata(resultAcrList[0],
                                                     resultAcrList[1], imgPath)
		imgFile = resultAcrList[0] + " - " + resultAcrList[1] + ".jpg"
		songLyrics = lyrics.get_metadata(resultAcrList[0], resultAcrList[1])
		songFile = modifier.get_songFile(path+x)
		# fileSong, track, artist, album, gender, year, track_number, lyrics, imgFile
		if resultSpotiList is not None:
			modifier.modify_file(songFile, imgPath,
                                             resultAcrList[0], resultAcrList[1], resultSpotiList[2],
                                             resultAcrList[3], resultAcrList[2], resultSpotiList[5],
                                             songLyrics, imgFile)
		else:
			modifier.modify_file(songFile, imgPath, resultAcrList[0],
                                             resultAcrList[1], resultAcrList[0]+" - Single",
                                             resultAcrList[3], resultAcrList[2], "1", songLyrics, "")
