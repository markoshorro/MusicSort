#!/usr/bin/env python

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC

class FileModifier:

	def get_songFile(self, filename):
		return MP3(filename, ID3=ID3)

	def modify_file(self, fileSong, imgPath, track, artist,
					album, gender, year, track_number, lyrics, imgFile):
		try:
		    fileSong.add_tags()
		except error:
		    pass

		fileSong["TIT2"] = TIT2(encoding=3, text=track)
		fileSong["TALB"] = TALB(encoding=3, text=album)
		fileSong["TPE2"] = TPE2(encoding=3, text=artist) #Artista del album
		fileSong["TPE1"] = TPE1(encoding=3, text=artist)	#Artista
		fileSong["TCON"] = TCON(encoding=3, text=gender)
		fileSong["TDRC"] = TDRC(encoding=3, text=year)
		fileSong["USLT"] = USLT(encoding=3, text=lyrics)
		if (imgFile != ""):
			fileSong.tags.add(
			    APIC(
			        encoding=3, # 3 para utf-8
			        mime='image/jpg', # tipo imagen
			        type=3, # 3 para la imagen
			        desc=u'Cover',
			        data=open(imgPath+imgFile).read()
			    )
			)
		fileSong.save()
