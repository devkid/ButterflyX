from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3

import Cover

class LibraryTrack:
	def __init__ (self):
		pass

class LibraryAlbum:
	
	def __init__ (self):
		self.tracks = {}
		self.coverCache = None
		pass

class LibraryArtist:
	
	def __init__ (self):
		self.albums = {}
		pass

class Library:
	def __init__ (self, app):
		self.app = app
		self.dbconn = app.dbconn
		
		# load sources
		self.sources = []
		self.dbconn.execute ("SELECT ID, name, path FROM Sources WHERE enabled = 1")
		for source in self.dbconn:
			self.sources.append ((source [0], source [1], source [2]))
		
		# load tracks
		# ID, path, album, tagTitle, tagArtist, tagYear, tagLength, tagNum, tagVolume, xListened, xRated, Albums.ID, Albums.name
		self.tracks = {}
		self.app.dbconn.execute ("SELECT * FROM Tracks INNER JOIN Albums ON Tracks.album = Albums.ID ORDER BY tagArtist ASC")
		artist = None
		album = None
		for track in self.dbconn:
			t = LibraryTrack ()
			t.dbID = track [0]
			t.path = track [1]
			t.title = track [3]
			t.artist = track [4]
			t.album = track [12]
			t.year = track [5]
			t.num = track [7]
			t.vol = track [8]
			t.listened = track [9]
			t.rated = track [10]
			
			if not t.artist in self.tracks.keys ():
				artist = self.tracks [t.artist] = LibraryArtist ()
				artist.name = t.artist
			else:
				artist = self.tracks [t.artist]
			
			if not t.album in artist.albums.keys ():
				album = artist.albums [t.album] = LibraryAlbum ()
				album.name = t.album
				album.cover = track [13]
				album.coverCache = track [14]
			else:
				album = artist.albums [t.album]
			
			album.tracks [t.title] = t
	
	def insertStatement (self, **kwargs):
		fields = ""
		values = ""
		first = True
		for field in kwargs:
			if first:
				first = False
			else:
				fields += ", "
				values += ", "
			fields += field
			values += str (kwargs [field])
		return "(%s) VALUES (%s)" % (fields, values)
		
	def addTrack (self, track):
		
		# look if we have an entry yet
		self.dbconn.execute ("SELECT ID FROM Tracks WHERE path = '%s'" % track.path)
		if self.dbconn.fetchone () != None:
			return
		
		tag = track.tag
		
		if tag ["album"] [0] == "":
			album = "\"" + tag ["album"] [0] + "\""
		else:
			album = "NULL"
		
		if tag ["date"] [0] == None:
			year = tag ["date"] [0]
		else:
			year = -1
		
		# look for album
		albumid = "NULL"
		if album != "NULL":
			self.dbconn.execute ("SELECT ID, cover, coverCache FROM Albums WHERE name = %s" % album)
			res = self.dbconn.fetchone ()
			hasCover = False
			if res == None:
				self.dbconn.execute ("INSERT INTO Albums (name) values ("+album+")")
				albumid = self.dbconn.lastrowid
			else:
				albumid = res [0]
				if res [1] != None:
					hasCover = True
		
		if not hasCover:
			cover = Cover.Cover (track.path)
			if cover.img != None:
				ba = QByteArray ()
				buffer = QBuffer (ba)
				buffer.open (QIODevice.WriteOnly)
				cover.img = QImage (QPixmap.fromImage (cover.img).scaled (QSize (50, 50), Qt.KeepAspectRatio, Qt.SmoothTransformation))
				cover.img.save (buffer, "jpg")
				
				self.dbconn.execute ("UPDATE Albums SET cover = '%s', coverCache = ? WHERE ID = %d" % (cover.filename, albumid), [sqlite3.Binary (str (ba))])
		
		# get length
		
		# insert new Track
		self.dbconn.execute ("INSERT INTO Tracks " + self.insertStatement (
			path		= "\"" + track.path + "\"",
			album		= albumid,
			tagTitle	= "\"" + tag ["title"] [0] + "\"",
			tagArtist	= "\"" + tag ["artist"] [0] + "\"",
			tagYear		= tag ["date"] [0],
			tagLength	= track.length,
			tagNum		= tag ["tracknumber"] [0]
			#tagVolume	= tag ["discnumber"] [0]
		))
		
		self.app.db.commit ()
