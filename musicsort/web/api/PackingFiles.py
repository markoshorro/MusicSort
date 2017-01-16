import os, zipfile
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import shutil
import StringIO

from musicsort.settings import *

# PRECOND: first value is valid
def sort_songs(user, params):
	if params[0]=="None":
		return False
	
	songsListPath= SESSION + '/' + str(user) + '.csv'
	df=pd.read_csv(songsListPath, sep='|',
                   names=['title', 'album',
			  'artist', 'year',
                          'genre', 'path'])
	
	MED_PATH = MEDIA_ROOT + '/'
    # print [x for x in params if x!="None"]
	grouped = df.groupby([x for x in params if x!="None"])
	
	for (subdirs), group in grouped:
		REL_PATH = str(user) + '/'
		if not type(subdirs) is tuple:
			subdirs = [subdirs]
		for i in subdirs:
			REL_PATH += str(i) + '/'
			if not os.path.exists(MED_PATH + REL_PATH):
				os.makedirs(MED_PATH + REL_PATH)
		for song in group.index.values:
			old_path = group.path[song]
			title = group.title[song]
			shutil.move(old_path, MED_PATH + REL_PATH + title + '.mp3')

	return True
