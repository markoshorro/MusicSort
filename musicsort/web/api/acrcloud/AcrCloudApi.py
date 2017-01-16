#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
    >>> python test.py test.mp3
'''

import os, sys
import json
from recognizer import ACRCloudRecognizer

class AcrCloudApi:
   
    def recognize_song(self, inputFile):
        config = {
            'host':'eu-west-1.api.acrcloud.com',
            'access_key':'97766ddcfc5edaa886b1b0d94f8b92f2',
            'access_secret':'OA5BUAWh0Yj7sQT9yVkBKtXUSEbVP1a1MDXB0bfR',
            'debug':False,
            'timeout':5 # seconds
        }
        
        # genresList = []
        inputFileSplit = []

        '''This module can recognize ACRCloud by most of audio/video file. 
            Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
            Video: mp4, mkv, wmv, flv, ts, avi ...'''
        re = ACRCloudRecognizer(config)
        # print "recognizing by file ..."
        # inputFile = sys.argv[1]
        #recognize by file path, and skip X seconds from from the beginning of inputFile.
        X = 0
        if re.recognize_by_file( inputFile, X) == "":
            inputFileSplit = inputFile.split("/")
            print "API ACRCloud: No se reconoce el archivo \"" + inputFileSplit[-1] + "\" como audio."
            return None
        else:
            results = json.loads(re.recognize_by_file( inputFile, X))
        if results['status']['msg'] == "Success":
            title = results['metadata']['music'][0]['title']
            artist = results['metadata']['music'][0]['artists'][0]['name']
            year = ""
            if 'release_date' in results['metadata']['music'][0]:
                release_date = results['metadata']['music'][0]['release_date']
                year = release_date[0:4]
            gender = ""
            if 'genres' in results['metadata']['music'][0]:
                gender = results['metadata']['music'][0]['genres'][0]['name']
            # for i in range(0, len(results['metadata']['music'][0]['genres'])):
            #     genresList.append(results['metadata']['music'][0]['genres'][i]['name'])
            return title, artist, year, gender  #genresList
        else:
            inputFileSplit = inputFile.split("/")
            print "API ACRCloud: No existen coincidencias para el archivo \"" + inputFileSplit[-1] + "\"."
            return None

        '''
        # Another way that recognize by buffer
        # inputFile must be in format: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz
        inputFile = sys.argv[1]
        buf = open( inputFile, 'rb').read()
        print "recognizing by buffer ..."
        #recognize by file_audio_buffer that read from file path, and skip X seconds from from the beginning of sys.argv[1].
        X = 0
        print re.recognize_by_filebuffer(buf, X)
        '''
