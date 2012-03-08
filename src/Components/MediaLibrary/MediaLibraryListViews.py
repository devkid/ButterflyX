from PyQt4.QtCore import *
from PyQt4.QtGui import *

import __init__ as MediaLibrary

import Library

app = QApplication.instance ()

def sortedDictValues1(adict):
    keys = adict.keys()
    keys.sort()
    return [key for key in keys]

def addAlbums (artist):
	global viewAlbums
	for al, album in artist.albums.items ():
		widget = MediaLibrary.AlbumWidget (album)
		alItem = QTreeWidgetItem ([""])
		alItem.setData (0, Qt.UserRole, album)
		viewAlbums.addTopLevelItem (alItem)
		viewAlbums.setItemWidget (alItem, 0, widget)

def addTracks (album):
	global viewTracks
	for tr, track in album.tracks.items ():
		widget = MediaLibrary.TrackWidget (track)
		trItem = QTreeWidgetItem ([""])
		trItem.setData (1, Qt.UserRole, track)
		viewTracks.addTopLevelItem (trItem)
		viewTracks.setItemWidget (trItem, 1, widget)

def activatedItem (item, column):
	global app, viewTracks
	app.handlePlayRequest (viewTracks.itemWidget (item, 1).track.path)

#
# viewArtists Widget
#

def changedArtist (cur, prev):
	global app, artist, viewAlbums
	
	if cur == None:
		return

	artist = cur.data (0, Qt.UserRole).toPyObject ()

	for i in range (viewAlbums.topLevelItemCount () - 1, -1, -1):
		viewAlbums.takeTopLevelItem (i)

	a = Library.LibraryAlbum ()
	a.name = _("All albums")
	widget = MediaLibrary.AlbumWidget (a)
	allAlbums = QTreeWidgetItem ([""])
	allAlbums.setData (0, Qt.UserRole, None)
	viewAlbums.addTopLevelItem (allAlbums)
	viewAlbums.setItemWidget (allAlbums, 0, widget)

	if not isinstance (artist, Library.LibraryArtist):
		for ar in sortedDictValues1 (app.library.tracks):
			addAlbums (app.library.tracks [ar])
	else:
		addAlbums (artist)

	viewAlbums.setCurrentItem (viewAlbums.topLevelItem (0))

viewArtists = QTreeWidget ()
viewArtists.header ().hide ()
viewArtists.currentItemChanged.connect (changedArtist)

a = Library.LibraryArtist ()
a.name = _("All artists")
widget = MediaLibrary.ArtistWidget (a, True)
allArtists = QTreeWidgetItem ([""])
allArtists.setData (0, Qt.UserRole, None)
viewArtists.addTopLevelItem (allArtists)
viewArtists.setItemWidget (allArtists, 0, widget)

for ar in sortedDictValues1 (app.library.tracks):
	artist = app.library.tracks [ar]
	widget = MediaLibrary.ArtistWidget (artist)
	arItem = QTreeWidgetItem ([""])
	arItem.setData (0, Qt.UserRole, artist)
	viewArtists.addTopLevelItem (arItem)
	viewArtists.setItemWidget (arItem, 0, widget)


#
# viewAlbums Widget
#

def changedAlbum (cur, prev):
	global app, artist, viewTracks
	
	if cur == None:
		return

	album = cur.data (0, Qt.UserRole).toPyObject ()

	for i in range (viewTracks.topLevelItemCount () - 1, -1, -1):
		viewTracks.takeTopLevelItem (i)

	if not isinstance (album, Library.LibraryAlbum):
		if not isinstance (artist, Library.LibraryArtist):
			for ar in sortedDictValues1 (app.library.tracks):
				for al in sortedDictValues1 (app.library.tracks [ar].albums):
					addTracks (app.library.tracks [ar].albums [al])
		else:
			for al in sortedDictValues1 (artist.albums):
				addTracks (artist.albums [al])
	else:
		addTracks (album)

viewAlbums = QTreeWidget ()
viewAlbums.header ().hide ()
viewAlbums.currentItemChanged.connect (changedAlbum)


#
# viewTracks Widget
#

viewTracks = QTreeWidget ()
viewTracks.itemActivated.connect (activatedItem)
viewTracks.setHeaderLabels (["","#", _("Title"), _("Album")])
viewTracks.header ().resizeSection (0, 30)
viewTracks.setRootIsDecorated (False)

viewArtists.setCurrentItem (viewArtists.itemAt (0, 0))

app.mainwindow.loaderInner.registerWidget ("viewArtists", viewArtists)
app.mainwindow.loaderInner.registerWidget ("viewAlbums", viewAlbums)
app.mainwindow.loaderInner.registerWidget ("viewTracks", viewTracks)

def createMediaLibraryView ():
	hsplitter = QSplitter (Qt.Horizontal)
	vsplitter = QSplitter (Qt.Vertical)

	hsplitter.addWidget (viewArtists)
	hsplitter.addWidget (vsplitter)

	vsplitter.addWidget (viewAlbums)
	vsplitter.addWidget (viewTracks)

	return hsplitter

app.mainwindow.setInnerLayout ("music", createMediaLibraryView)