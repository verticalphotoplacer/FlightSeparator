# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Flight Separator
                                 A Standalone Desktop Application
 This tool performs separation of a list of photos into flights
                              -------------------
        begin                : 2020-09-01
        git sha              : 
        copyright            : (C) 2020 by Chubu University
        email                : ts18851@chubu.ac.jp
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtWidgets import QMessageBox, QLineEdit
from os.path import isdir

class FolderEdit(QLineEdit):
    def __init__(self, parent):
        super(FolderEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            if isdir(filepath):
                self.setText(filepath)
            else:
                dialog = QMessageBox()
                dialog.setSizeGripEnabled(True)
                dialog.setWindowTitle("Error: Invalid Input")
                dialog.setText("Only folder is accepted")
                dialog.setIcon(QMessageBox.Warning)
                dialog.exec_()