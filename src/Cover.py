import os, mimetypes, string

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import mutagen.id3

import Track

class Cover:
	
	def __init__ (self, filename):
		
		methods = [self.searchID3, self.searchFolder]
		
		self.img = None
		self.filename = ""
		
		for m in methods:
			if m (filename):
				break
	
	def searchID3 (self, filename):
		
		tag = Track.FileTrack (filename, False).tag.tags
		if tag == None or len (tag) < 1:
			return False
			
		if isinstance (tag, mutagen.id3.ID3):
			images = tag.getall ('APIC')
			img = None
			for i in images:
				if i.type == 3:
					img = i
			if img == None:
				if len (images) > 0:
					img = images [0]
				else:
					return False
			
			self.img = QImage.fromData (img.data)
			self.filename = "infile"
			
			return True
		else:
			return False
			
	
	def searchFolder (self, filename):
		
		folder = os.path.dirname (filename)
		files = os.listdir (folder)
		
		album = Track.FileTrack (filename).tag ["album"]
		
		found = False
		for f in files:
			t = mimetypes.guess_type (f) [0]
			if t == None:
				continue
			t = string.split (t, '/', 1) [0]
			
			fname = folder + '/' + f
			
			if t == 'audio':
			
				tag = Track.FileTrack (folder + "/" + f).tag
				
				if album == '':
					album = tag.getAlbum ()
				elif tag ["album"] != album:
					return False
			
			if not found and t == 'image':
				img = QImage (fname)
				filname = fname
				found = True
		
		if found:
			self.img = img
			self.filename = filename
		
		return False
