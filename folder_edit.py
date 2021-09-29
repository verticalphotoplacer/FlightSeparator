# -*- coding: utf-8 -*-
"""
/******************************************************************************************
 Flight Separator
                                 A Standalone Desktop Application
 This tool detects and separates drone photos in a folder taken in
 different flights based on timestamps.
                              -------------------
        begin                : 2020-09-01
        copyright            : (C) 2019-2021 by Chubu University and
               National Research Institute for Earth Science and Disaster Resilience (NIED)
        email                : chuc92man@gmail.com
 ******************************************************************************************/

/******************************************************************************************
 *   This file is part of Flight Separator.                                               *
 *                                                                                        *
 *   This program is free software; you can redistribute it and/or modify                 *
 *   it under the terms of the GNU General Public License as published by                 *
 *   the Free Software Foundation, version 3 of the License.                              *
 *                                                                                        *
 *   Flight Separator is distributed in the hope that it will be useful,                  *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or    *
 *   FITNESS FOR A PARTICULAR PURPOSE.                                                    *
 *   See the GNU General Public License for more details.                                 *
 *                                                                                        *
 *   You should have received a copy of the GNU General Public License along with         *
 *   Flight Separator. If not, see <http://www.gnu.org/licenses/>.                        *
 ******************************************************************************************/
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