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

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, QDateTime, Qt
from PyQt5.uic import loadUiType

import traceback, sys
from os.path import abspath, join

import resources_rc
import folder_edit
from flight_separator import flightSeparator

MAX_THREADS = 2


def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)


FORM_CLASS,_ = loadUiType(resourcePath('main.ui'))


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.func(self.args[0], self.args[1], self.args[2], self.args[3], **self.kwargs)
        except:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Main(QMainWindow, FORM_CLASS):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(join(resourcePath('icon'), 'app.png')))
        self.setupUi(self)
        self.Handel_Buttons()

        # initialize input variables
        self.fs_folder_name = None
        self.fs_stime = 1
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(MAX_THREADS)

    def Handel_Buttons(self):
        self.fs_intext.textChanged.connect(self.onIntextChanged)
        self.fs_inbutton.clicked.connect(self.onSelectPhotoFolder)
        self.fs_timesbox.valueChanged.connect(self.onSetFStime)
        self.fs_button_box.accepted.connect(self.onAccept)
        self.fs_button_box.rejected.connect(self.onClosePlugin)
        self.fs_clearlog.clicked.connect(self.onClearLog)
        self.fs_copylog.clicked.connect(self.onCopyLog)
        self.fs_savelog.clicked.connect(self.onSaveLog)
        self.fs_clearlog.setIcon(QIcon(join(resourcePath('icon'), 'erase.png')))
        self.fs_copylog.setIcon(QIcon(join(resourcePath('icon'), 'copypaste.png')))
        self.fs_savelog.setIcon(QIcon(join(resourcePath('icon'), 'save2file.png')))

    def onIntextChanged(self):
        """
        Callback for LineEdit change, set content to self.fs_folder_name.

        Returns
        -------
        None.

        """

        self.fs_folder_name = self.fs_intext.text()
        self.fs_progress.setValue(0)

    def onSelectPhotoFolder(self):
        """
        Set content for self.fs_intext when user choose folder via button.

        Returns
        -------
        None.

        """

        folder = QFileDialog.getExistingDirectory(self, "Select folder ")
        # if user do not select any folder, then don't change folder_name
        if len(folder) > 1:
            self.fs_intext.setText(folder)

    def onSetFStime(self, new_value):
        """
        Set flight separation time.

        Parameters
        ----------
        new_value : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        self.fs_stime = int(new_value)

    def onAccept(self):
        """
        Flight separator processing.

        Returns
        -------
        None.

        """

        if self.fs_folder_name is not None:
            c_fs_stime = self.fs_stime * 60
            iskeep = self.fs_checkbox.isChecked()
            worker = Worker(flightSeparator, self.fs_folder_name, (".jpg"), c_fs_stime, iskeep)
            worker.signals.result.connect(self.onWriteLog)
            worker.signals.progress.connect(self.onProgressUpdate)
            worker.signals.error.connect(self.onError)
            self.threadpool.start(worker)

    def onProgressUpdate(self, n):
        """
        Update processing progress.

        Parameters
        ----------
        n : float
            Percentage of work done.

        Returns
        -------
        None.

        """

        self.fs_progress.setValue(int(n))

    def onError(self, e):
        """
        Processing with exception.

        Parameters
        ----------
        e : Exception
            Exception encounted during processing.

        Returns
        -------
        None.

        """

        self.fs_log.appendPlainText("{0}: Task completed!\n {1}\n".format(QDateTime.currentDateTime().toString(Qt.ISODate), e[1]))

    def onWriteLog(self, result):
        """
        Write results to log widget.

        Parameters
        ----------
        result : string
            Log string.

        Returns
        -------
        None.

        """

        self.fs_log.appendPlainText("{0}: Task completed!\n {1}\n".format(QDateTime.currentDateTime().toString(Qt.ISODate), result["msg"]))

    def onClearLog(self):
        """
        Clear log widget.

        Returns
        -------
        None.

        """

        self.fs_log.clear()

    def onCopyLog(self):
        """
        Copy log content.

        Returns
        -------
        None.

        """

        self.fs_log.selectAll()
        self.fs_log.copy()

    def onSaveLog(self):
        """
        Save log content to a file.

        Returns
        -------
        None.

        """

        try:
            name = QFileDialog.getSaveFileName(self, "Save File", '/', '.txt')[0]
            with open(name, 'w') as f:
                f.write(str(self.fs_log.toPlainText()))
        except:
            return

    def onClosePlugin(self):
        """
        Close the application.

        Returns
        -------
        None.

        """

        self.close()

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()
