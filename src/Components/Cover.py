import os, mimetypes, string

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import eyeD3

import Track

class Cover (QLabel):
	
	def __init__ (self, app):
		super (QLabel, self).__init__ ()
		self.app = app
		self.app.trackChanged.connect (self.onChanged)
		
		self.resize (200, 200)
		
		self.pm = None
	
	def resizeEvent (self, QResizeEvent):
		if self.pm <> None:
			self.setPixmap (self.pm.scaled (self.size (), Qt.KeepAspectRatio, Qt.SmoothTransformation))
	
	def onChanged (self, obj):
		
		methods = [self.searchID3, self.searchFolder]
		
		for m in methods:
			if m (obj):
				break
		
		self.resizeEvent (None)
	
	def searchID3 (self, obj):
		
		images = obj.tag.getImages ()
		img = None
		for i in images:
			if i.pictureType == eyeD3.ImageFrame.FRONT_COVER:
				img = i
		if img == None:
			if len (images) > 0:
				img = images [0]
			else:
				return False
		
		self.pm = QPixmap.fromImage (QImage.fromData (img.imageData))
		
		return True
	
	def searchFolder (self, obj):
		
		if isinstance (obj, Track.FileTrack) == False:
			return False
		
		folder = os.path.dirname (obj.path)
		files = os.listdir (folder)
		
		album = obj.tag.getAlbum ()
		
		found = False
		for f in files:
			t = mimetypes.guess_type (f) [0]
			if t == None:
				continue
			t = string.split (t, '/', 1) [0]
			
			fname = folder + '/' + f
			
			if t == 'audio':
			
				tag = eyeD3.Tag ()
				tag.link (fname)
				
				if album == '':
					album = tag.getAlbum ()
				elif tag.getAlbum () <> obj.tag.getAlbum ():
					return False
			
			if not found and t == 'image':
				print f
				self.pm = QPixmap (fname)
				print self.pm
				found = True
		
		return False