from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4.phonon import Phonon

import Track

class Player (QObject):
	def __init__ (self, app):
		QObject.__init__ (self)
		self.app = app
		
		self.out = Phonon.AudioOutput (Phonon.MusicCategory, self.app)
		self.media = Phonon.MediaObject (self.app)
		self.media.prefinishMark = 1000
		Phonon.createPath (self.media, self.out)
	
	def play (self, source):
		self.media.stop ()
		self.media.setCurrentSource (source)
		self.media.play ()
	
	def enqueue (self, source):
		self.media.enqueue (source)
