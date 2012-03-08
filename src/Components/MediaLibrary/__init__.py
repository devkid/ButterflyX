from PyQt4.QtCore import *
from PyQt4.QtGui import *

import MediaLibraryListViews
import MediaLibraryTreeView

class ArtistWidget (QLabel):

	def __init__ (self, artist, bold = False):

		if isinstance (artist, str):
			name = artist
		else:
			name = artist.name

		if bold:
			QLabel.__init__ (self, '<b>' + name + '</b>')
		else:
			QLabel.__init__ (self, name)

		self.artist = artist
		self.setMargin (5)
		self.setTextFormat (Qt.RichText)

class AlbumWidget (QWidget):

	def __init__ (self, album):
		QWidget.__init__ (self)
		self.album = album

		self.vbox = QHBoxLayout (self)

		self.cover = QLabel ()
		self.cover.resize (40, 40)
		if album.coverCache <> None:
			pm = QPixmap.fromImage (QImage.fromData (album.coverCache))
		else:
			pm = QPixmap ("images/unknownCover.png")
		self.cover.setPixmap (pm.scaled (self.cover.size (), Qt.KeepAspectRatio, Qt.SmoothTransformation))

		self.label = QLabel (album.name)
		self.label.setAlignment (Qt.AlignLeft | Qt.AlignVCenter)

		self.vbox.addWidget (self.cover)
		self.vbox.addWidget (self.label)
		self.vbox.setAlignment (Qt.AlignLeft)

class TrackWidget (QLabel):

	def __init__ (self, track):
		QLabel.__init__ (self, track.title)
		self.track = track
		self.setMargin (5)