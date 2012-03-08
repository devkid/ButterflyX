#!/usr/bin/python
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

import sys, os, errno, signal, string, Queue
import gettext

import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon

import Track
import Library
import Player
import Source
import MainWindow

class App (QApplication):
	
	trackChanged = pyqtSignal (object)
	
	currentTrack = None
	
	def __init__ (self):
		QApplication.__init__ (self, sys.argv)
		self.setApplicationName ("MP")
		signal.signal (signal.SIGINT, signal.SIG_DFL)
		
		self.readConfig ()
		
		self.library = Library.Library (self)
		self.player = Player.Player (self)
		
		self.queue = Queue.Queue ()
		
		self.player.media.prefinishMarkReached.connect (self._enqueue)
		
		self.mainwindow = MainWindow.MainWindow (self)
	
	def readConfig (self):
		try:
			
			home = os.getenv ("HOME")
			configDir = home + '/.mp'
			
			if not os.path.isdir (configDir):
				os.mkdir (configDir)

			if not os.path.isdir (configDir + '/layouts'):
				os.mkdir (configDir + '/layouts')
			
			self.db = sqlite3.connect (configDir + '/mp.db')
			self.dbconn = self.db.cursor ()
			self.dbconn.execute ("PRAGMA foreign_keys = ON")
			
			self.setupTables ()
		
		except (OSError, sqlite3.OperationalError):
			#box = QMessageBox (QMessageBox.Critical, _("Configuration error"), _(u"There seems to be an error accessing the configuration directory of MP.<br /><br />You can find this folder in your home directory, it is named ».mp«. Most likely this folder is hidden, so you have to enable the »Show hidden files« option in your file browser. Please make sure you have permissions to read and write in your home directory and in this ».mp« folder (if it exists).<br /><br />If you can't solve the problem on your own, please feel free to ask for support on <a href=\"http://mp.devkid.net/\">http://mp.devkid.net/</a>.<br /><br />To find out more about this error, try to run »mp« from a terminal program and watch its output."))
			#box.exec_ ()
			raise
	
	def setupTables (self):
		tables = [
			("Plugins", [
				"ID			INTEGER primary key autoincrement",
				"name		TEXT",
				"enabled	BOOLEAN"]),
			("Sources", [
				"ID			INTEGER primary key autoincrement",
				"name		TEXT",
				"path		TEXT",
				"enabled	BOOLEAN"]),
			("Albums", [
				"ID			INTEGER primary key autoincrement",
				"name		TEXT",
				"cover		TEXT",
				"coverCache	BLOB"]),
			("TrackArtists", [
				"track		INTEGER",
				"artist		INTEGER",
				"FOREIGN KEY (track) REFERENCES Tracks (ID)",
				"FOREIGN KEY (artist) REFERENCES Artist (ID)"]),
			("Tracks", [
				"ID			INTEGER primary key autoincrement",
				"path		TEXT not null",
				"album		INTEGER",
				"tagTitle	TEXT",
				"tagArtist	TEXT",
				"tagYear	INTEGER",
				"tagLength	INTEGER",
				"tagNum		INTEGER",
				"tagVolume	TEXT",
				"xListened	INTEGER not null default 0",
				"xRated		INTEGER not null default 0",
				"FOREIGN KEY (album) REFERENCES Albums (ID)"])
			]
		for t in tables:
			self.dbconn.execute ("CREATE TABLE IF NOT EXISTS " + t [0] + "(" + string.join (t [1], ",") + ")")
	
	def _late_init (self):
		self.player._late_init ()
		pass
	
	def handlePlayRequest (self, request):
		url = QUrl (request)
		
		if url.scheme () in ("", "file"):
			if url.scheme () == "":
				url.setScheme ("file")
			self.player.media.stop ()
			self.player.play (Phonon.MediaSource (url))
			self.trackChanged.emit (url.path ())
	
	def playpause (self):
		if self.player.media.state () == Phonon.PlayingState:
			self.player.media.pause ()
		else:
			if self.player.media.state () == Phonon.PausedState or self._enqueue ():
				self.player.media.play ()
	
	def skip (self):
		self.player.media.stop ()
		self.player.media.clearQueue ()
		if not self.queue.empty ():
			path = self.queue.get ()
			self.player.media.setCurrentSource (Phonon.MediaSource (path))
			self.player.media.play ()
			self.trackChanged.emit (path)
		else:
			self.trackChanged.emit (None)
	
	def enqueue (self, track):
		self.queue.put (track)
	
	def _enqueue (self):
		if not self.queue.empty ():
			path = self.queue.get ()
			self.player.media.enqueue (Phonon.MediaSource (path))
			self.trackChanged.emit (path)
			return True
		else:
			self.trackChanged.emit (None)
			return False


gettext.install ("mp", unicode=1)

app = App ()

import Components

app.mainwindow.load ()

app.library.addTrack (Track.FileTrack ("/home/devkid/Musik/The Lion King Musical - Original Broadway Cast Recording FLAC/01 - The Lion King Cast - Circle Of Life.flac"))
app.library.addTrack (Track.FileTrack ("/home/devkid/Musik/The Lion King Musical - Original Broadway Cast Recording FLAC/02 - The Lion King Cast - Grasslands Chant.flac"))
app.library.addTrack (Track.FileTrack ("/home/devkid/Musik/Lana Del Rey/Born To Die/04 - Video Games.mp3"))
app.library.addTrack (Track.FileTrack ("/home/devkid/Musik/Aura Dione/Before The Dinosaurs/03 - Friends.mp3"))

app.exec_ ()
