from PyQt4.QtCore import *
from PyQt4.phonon import Phonon
import mutagen

class Track (QObject):
	
	def __init__ (self, tag, source, path, length):
		super (QObject, self).__init__ ()
		self.tag = tag
		self.source = source
		self.path = path
		self.length = length
	
	def getMediaSource (self):
		return self.source
	

class FileTrack (Track):
	
	def __init__ (self, filename, easy=True):
		
		tag = mutagen.File (filename, easy=easy)
		length = -1
		
		Track.__init__ (self, tag, Phonon.MediaSource (filename), filename, length)


class StreamTrack (Track):
	
	def __init__ (self, url):
		self.url = url
		
		tag = eyeD3.Tag ()
		
		AudioObject.__init__ (self, tag, Phonon.MediaSource (QUrl (url)), url, -1)

