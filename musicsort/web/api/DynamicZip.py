from musicsort.settings import MEDIA_ROOT
import StringIO, zipfile, os

def make_zip(user):

	folder = MEDIA_ROOT + '/' + str(user) + '/'
         
    # Open StringIO to grab in-memory ZIP contents
	output_file = StringIO.StringIO()
         
    # The zip compressor
	zf = zipfile.ZipFile(output_file, "w")

	basedir = os.path.join(MEDIA_ROOT, str(user))
	for root, dirs, files in os.walk(folder):        
		dirname = root.replace(basedir, '')
		if dirname=='/img':
			continue
		for f in files:
			zf.write(root + '/' + f, dirname + '/' + f)		 

	zf.close()
        
	return output_file
