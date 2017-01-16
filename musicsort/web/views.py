# for drag and drop
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from forms import UploadFileForm
from models import UploadFile
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect 

from musicsort.settings import *

from api import PackingFiles, DynamicZip
from api.Processor import Processor

import os, sys, shutil

import StringIO, zipfile

#############################################
# Main view
@csrf_protect
def index(request):
	return render(request,'web/index.html')

#############################################
# Called every time is refreshed the page
@csrf_protect
def delete_user_file(request):
	if os.path.exists(MEDIA_ROOT + '/' + str(request.user) + '/'):
		shutil.rmtree(MEDIA_ROOT + '/' + str(request.user) 
				+ '/', ignore_errors=False, onerror=None)
				
	return render(request,'web/index.html')

#############################################
# Registering users
@csrf_protect
def register(request):
    data = {}
    data['error'] = 0
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Registrado correctamente')
            response = HttpResponseRedirect("/web/")
            return response
        else:
			# use messages here as well
            data['error'] = 1
            data['error_msg'] = "Error en credenciales"
    else:
        form = UserCreationForm()
                
    data['form'] = form
    return render(request, "registration/register.html", data) 

#############################################
# View for uploading files
@csrf_protect
def dragdrop(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(user = request.user, file = request.FILES['file'])
            new_file.user = request.user
            new_file.save()
            response = HttpResponse('index')
            return response
        else:      
            form = UploadFileForm()
            
    data = {'form': form}

    return render_to_response('web/index.html', data,
							  context_instance=RequestContext(request))

#############################################
# Called every time a file is deleted
@csrf_protect
def del_file(request):
    UploadFile.objects.filter(user = request.user).delete()
    path = MEDIA_ROOT + "/" + str(request.user)
    try:
        if os.path.exists(path):
            if not os.listdir(path)=="":
                shutil.rmtree(path)
    except OSError as err:
        pass

    return HttpResponseRedirect(reverse('index'))

#############################################
# Called for asking for sorting and zipping songs
@csrf_protect
def process_songs(request):
	# here it is processed the request
	if request.is_ajax():
		request_data = request.POST
		index1 = request_data['index1']
		index2 = request_data['index2']
		lyrics = request_data['lyrics']=='true'
		Processor.process_all_songs(request.user, lyrics)
		# it is possible to check whether the value is true or false
		out = PackingFiles.sort_songs(request.user, [index1, index2])
		# ok!
		return HttpResponse()
	# after processing the view responses with the zip file
	else:
		output_file = DynamicZip.make_zip(request.user)
		# Grab ZIP file from in-memory, make response with correct MIME-type
		resp = HttpResponse(content_type = "application/zip")
		# ..and correct content-disposition
		resp['Content-Disposition'] = 'attachment; filename=%s' % "musicsort_" + str(request.user) + ".zip"
        
		output_file.seek(0)
		resp.write(output_file.read())
		if os.path.exists(MEDIA_ROOT + '/' + str(request.user) + '/'):
			shutil.rmtree(MEDIA_ROOT + '/' + str(request.user) 
				+ '/', ignore_errors=False, onerror=None)
		return resp
