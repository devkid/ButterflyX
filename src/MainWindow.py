# -*- coding: UTF-8 -*-

#
# Copyright (C) by Alfred Krohmer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import os

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from QRearrangeableLayout import QRearrangeableLayout
from QRearrangeableLayoutLoader import QRearrangeableLayoutLoader

import Library, Track

class MainWindow (QMainWindow):
	
	def __init__ (self, app):
		QMainWindow.__init__ (self)
		self.app = app

		self.innerName = ""
		
		self.setWindowTitle ("MP")

		self.setWindowState (Qt.WindowMaximized)
		
		#self.resize (800, 600)
		
		self.menuBar ().addMenu (_("&File")).addAction (_("Rearrange window contents")).triggered.connect (lambda:self.layoutOuter.setRearrangeable (not self.layoutOuter.rearrangeable ()))
		
		self.toolbar = self.addToolBar ("blub")
		self.toolbar.addAction (QIcon ("images/play.png"), _("Play")).triggered.connect (self.app.playpause)
		self.toolbar.addAction (QIcon ("images/skip.png"), _("Skip")).triggered.connect (self.app.skip)
		
		self.setupPlayingWidget ()
		self.toolbar.addWidget (self.playingWidget).setVisible (True)

		self.mainbox = QVBoxLayout ()
		self.central = QWidget ()
		self.central.setLayout (self.mainbox)
		self.setCentralWidget (self.central)

		self.layoutOuter = QRearrangeableLayout (app)
		self.layoutOuterBox = QHBoxLayout ()
		self.layoutOuterBox.setContentsMargins (QMargins (0, 0, 0, 0))
		self.layoutOuter.setLayout (self.layoutOuterBox)
		self.mainbox.addWidget (self.layoutOuter)

		self.layoutInner = QRearrangeableLayout (app)
		self.layoutInnerBox = QHBoxLayout ()
		self.layoutInnerBox.setContentsMargins (QMargins (0, 0, 0, 0))
		self.layoutInner.setLayout (self.layoutInnerBox)
		#self.layoutOuterBox.addWidget (self.layoutInner)

		# Navigation widget
		#self.navigation = Navigation.Navigation (self.app)

		# Loader
		self.loaderOuter = QRearrangeableLayoutLoader (self.layoutOuter)
		self.loaderInner = QRearrangeableLayoutLoader (self.layoutInner)

		self.loaderOuter.registerWidget ("innerLayout", self.layoutInner)

		self.show ()


	def load (self):
		self.loaderOuter.load (os.getenv ("HOME") + '/.mp/layoutOuter.xml')


	def closeEvent (self, event):
		if self.innerName != "":
			self.loaderInner.save (os.getenv ("HOME") + '/.mp/layouts/' + self.innerName + '.xml')
		self.loaderOuter.save (os.getenv ("HOME") + '/.mp/layoutOuter.xml')


	def setInnerLayout (self, name, initialCreate):

		if name == self.innerName:
			return

		# save old layout
		if self.innerName != "":
			self.loaderInner.save (os.getenv ("HOME") + '/.mp/layouts/' + self.innerName + '.xml')

		try:
			self.loaderInner.load (os.getenv ("HOME") + '/.mp/layouts/' + name + '.xml')
		except (IOError):
			widget = initialCreate ()

			self.layoutInner.layout ().removeItem (self.layoutInner.layout ().itemAt (0))
			self.layoutInner.layout ().addWidget (widget)

		self.innerName = name


	def setupPlayingWidget (self):
		
		self.playingWidget = QLabel (_("Stopped"))
		self.playingWidget.setMargin (5)
		
		self.app.trackChanged.connect (self.updatePlayingWidget)
	
	def updatePlayingWidget (self, track):
		
		if track == None:
			text = _("Stopped")
		else:
			text = _("Currently playing:") + " " + track
		
		self.playingWidget.setText (text)

	"""
	def setupTreeview (self):
		
		self.hsplitter = QSplitter (Qt.Horizontal, self.central)
		
		self.tv = QTreeWidget ()
		self.hsplitter.addWidget (self.tv)
		self.tv.resize (800, 600)
		self.tv.header ().hide ()

		#for ar, artist in self.app.library.tracks.items ():
		for ar in sortedDictValues1 (self.app.library.tracks):
			artist = self.app.library.tracks [ar]
			widget = ArtistWidget (artist)
			arItem = QTreeWidgetItem ([""])
			arItem.setData (0, Qt.UserRole, artist)
			self.tv.addTopLevelItem (arItem)
			self.tv.setItemWidget (arItem, 0, widget)
			
			for al, album in artist.albums.items ():
				widget = AlbumWidget (album)
				alItem = QTreeWidgetItem ([""])
				alItem.setData (0, Qt.UserRole, album)
				arItem.addChild (alItem)
				self.tv.setItemWidget (alItem, 0, widget)
			
				for t, track in album.tracks.items ():
					widget = TrackWidget (track)
					tItem = QTreeWidgetItem ([""])
					tItem.setData (0, Qt.UserRole, track)
					alItem.addChild (tItem)
					self.tv.setItemWidget (tItem, 0, widget)
		
		self.tv.itemActivated.connect (self.activated)
		
		self.queueview = QListWidget ()
		self.hsplitter.addWidget (self.queueview)
		#self.queueview.addItem (QListWidgetItem ("Test"))
		
		self.hsplitter.setSizePolicy (QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		self.hbox = QHBoxLayout ()
		self.central.setLayout (self.hbox)
		
		self.hbox.addWidget (self.hsplitter)
		
		self.show ()
	
	def activated (self, item, column):
		widget = item.data (0, Qt.UserRole).toPyObject ()
		paths = []
		if isinstance (widget, Library.LibraryTrack):
			#self.app.enqueue (widget.path)
			paths.append (widget.path)
		elif isinstance (widget, Library.LibraryAlbum):
			for track in widget.tracks.values ():
				#self.app.enqueue (track.path)
				paths.append (track.path)
		elif isinstance (widget, Library.LibraryArtist):
			for album in widget.albums.values ():
				for track in album.tracks.values ():
					#self.app.enqueue (track.path)
					paths.append (track.path)
		
		for p in paths:
			self.app.enqueue (track.path)
			self.queueview.addItem (QListWidgetItem (p))
	"""
