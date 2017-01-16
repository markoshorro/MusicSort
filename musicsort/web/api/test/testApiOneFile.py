#!/usr/bin/env python

import os, sys
from MetadataObtainer import MetadataSpotify
from acrcloud.AcrCloudTest import AcrCloudTest
from MusiXMatch import MusiXMatchLyrics
from FileModifier import FileModifier

metaD = MetadataSpotify()
acr = AcrCloudTest()
lyrics = MusiXMatchLyrics()
modifier = FileModifier()
resultAcrList = [] 
resultSpotiList = []
inputFile = sys.argv[1]
# title, artist, year, genresList
resultAcrList = acr.recognize_song(inputFile)
if resultAcrList is not None:
	# imgURL ,albumType ,albumName ,artistList ,explicit ,track_number
	resultSpotiList = metaD.get_metadata(resultAcrList[0], resultAcrList[1])
	imgFile = resultAcrList[0] + " - " + resultAcrList[1] + ".jpg"
	songLyrics = lyrics.get_metadata(resultAcrList[0], resultAcrList[1])
	songFile = modifier.get_songFile(inputFile)
	# fileSong, track, artist, album, gender, year, track_number, lyrics, imgFile
	if resultSpotiList is not None:
		modifier.modify_file(songFile, resultAcrList[0], resultAcrList[1], resultSpotiList[2], resultAcrList[3], resultAcrList[2], resultSpotiList[5], songLyrics, imgFile)
	else:
		modifier.modify_file(songFile, resultAcrList[0], resultAcrList[1], resultAcrList[0]+" - Single", resultAcrList[3], resultAcrList[2], "1", songLyrics, "")
