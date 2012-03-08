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

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

app = QApplication.instance ()

class Navigation (QTreeWidget):

	def __init__ (self, app):
		QTreeWidget.__init__ (self)

		self.header ().hide ()
		self.setRootIsDecorated (False)

		self.mediaLibrary = QTreeWidgetItem ([_("Media Library")])
		self.mediaLibrary.setFlags (Qt.ItemFlags (Qt.ItemIsEnabled))
		self.addTopLevelItem (self.mediaLibrary)
		self.setItemExpanded (self.mediaLibrary, True)

		self.mediaLibraryMusic = QTreeWidgetItem ([_("Music")])
		self.mediaLibraryMusic.setFlags (Qt.ItemIsEnabled | Qt.ItemIsSelectable)
		self.mediaLibrary.addChild (self.mediaLibraryMusic)

		self.app = app

app.mainwindow.loaderOuter.registerWidget ("navigation", Navigation (app))