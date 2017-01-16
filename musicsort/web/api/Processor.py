#!/usr/bin/env python

import os, sys
import threading
from multiprocessing import Process, Queue
from musicsort.settings import *
from MetadataObtainer import MetadataSpotify
from acrcloud.AcrCloudApi import AcrCloudApi
from MusiXMatch import MusiXMatchLyrics
from FileModifier import FileModifier

# This is the main class for processing songs
class Processor:
	@staticmethod
	def process_all_songs(user, lyrics):
		reload(sys)    # to re-enable sys.setdefaultencoding()
		sys.setdefaultencoding('utf-8')
		path = MEDIA_ROOT + '/' + str(user)
		q = Queue()
		if not (path.endswith("/")):
			path = path + "/"
		imgPath = path + "img/"
		if not os.path.exists(imgPath):
			os.makedirs(imgPath)
		files = os.listdir(path) 
		threadList = list()
		songsListPath= SESSION + '/' + str(user) + '.csv'
		if not os.path.exists(SESSION):
			os.makedirs(SESSION)
		songsList=open(songsListPath,'w')
		songsList.close()
		for x in files:
			if ("img" == str(x)):
				continue
			p = Process(target=Processor().process_song, args=(path,imgPath,x,lyrics,q))
			threadList.append(p)
			p.start()
	
		for p in threadList:
			songsList = open(songsListPath, 'a')
			d = q.get()
			songsList.write(d)
			songsList.close()
			p.join()	

	# q param is for qeueing
	@staticmethod
	def process_song(path, imgPath, song, lyrics, q):
		metaD = MetadataSpotify()
		acr = AcrCloudApi()
		lyrics = MusiXMatchLyrics() 
		modifier = FileModifier()
		resultAcrList = [] #0-title 1-artist  2-year  3-gender
		resultSpotiList = [] #0-imgURL  1-albumType  2-albumName 3-artistList 4-explicit 5-track_number
		songSplit = [] 
		resultAcrList = acr.recognize_song(path+song)
		pathForQ = path + song
		
		if resultAcrList is not None:
			# In case there are blank values
			resultAcrList = ['unknown' if r=='' else r for r in resultAcrList]
			
			# imgURL, albumType, albumName, artistList, explicit, track_number
			resultSpotiList = metaD.get_metadata(resultAcrList[0],
                                                             resultAcrList[1], imgPath)
			imgFile = resultAcrList[0] + " - " + resultAcrList[1] + ".jpg"
			songLyrics = ''
			if lyrics:
				songLyrics = lyrics.get_metadata(resultAcrList[0], resultAcrList[1])
			songFile = modifier.get_songFile(path+song)
			# fileSong, track, artist, album, gender, year, track_number, lyrics, imgFile
			if resultSpotiList is not None:
                                modifier.modify_file(songFile,imgPath,
                                                     resultAcrList[0],
                                                     resultAcrList[1],
                                                     resultSpotiList[2],
                                                     resultAcrList[3],
		                                     resultAcrList[2],
                                                     resultSpotiList[5],
                                                     songLyrics, imgFile)
			else:
				modifier.modify_file(songFile,imgPath, resultAcrList[0],
                                                     resultAcrList[1],
		                                     resultAcrList[0]+" - Single",
                                                     resultAcrList[3],
		                                     resultAcrList[2],
                                                     "1", songLyrics, "")
			songSplit = song.split(".")
 			new_title = resultAcrList[0] + " - " + resultAcrList[1] + "." + songSplit[-1]
			os.rename(path + song, path + new_title)
			
            # Title, Artist, Album, Year, Genre, Path
			if resultSpotiList is not None:
				q.put(resultAcrList[0] + '|' + resultSpotiList[2] + '|' + resultAcrList[1] + '|' + resultAcrList[2] +
                              '|' + resultAcrList[3] + '|' + path + new_title + '\n') 
			else:
				q.put(resultAcrList[0] + '|' + 'unknown' + '|' + resultAcrList[1] + '|' + resultAcrList[2] +
                              '|' + resultAcrList[3] + '|' + path + new_title + '\n') 
		
		else:
                        #Title, Artist, Album, Year, Genre, Path
			q.put(song + "|unknown|unknown|unknown|unknown|" +
                              pathForQ+"\n")   
			
