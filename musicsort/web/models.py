from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Needed for drag and drop
# https://amatellanes.wordpress.com/2013/11/05/dropzonejs-django-how-to-build-a-file-upload-form/
# https://docs.djangoproject.com/en/dev/ref/models/fields/#filefield

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return '{0}/{1}'.format(instance.user, filename)

class UploadFile(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 0)
	file = models.FileField(upload_to=user_directory_path)

	def __unicode__(self):
		return self.file.name
