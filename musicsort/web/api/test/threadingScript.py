#!/usr/bin/env python

import os, sys
import threading
from Processor import Processor
from multiprocessing import Process, Queue
from view import getUser

def ThreadsSongs(user):
	pro = Processor()
	path = sys.argv[1]
	q = Queue()
	if not (path.endswith("/")):
		path = path + "/"
	imgPath = path + "img/"
	if not os.path.exists(imgPath):
		os.makedirs(imgPath)
	files = os.listdir(path) 
	i = 0
	threadList = list()
	songsListPath= SESSION + str(user) + '.csv'   #falta meter el nombre de usuario entre lo '+'
	songsList=open(songsListPath,'w')
	songsList.close()
	for x in files:
		print "Processing song %d: " % i + x
		p = Process(target=pro.process_song, args=(path,imgPath,x,q))
		threadList.append(p)
		p.start()
		i += 1
	
	for p in threadList:
		songsList = open(songsListPath, 'a')
		d = q.get()
		songsList.write(d)
		songsList.close()
		p.join()
	
