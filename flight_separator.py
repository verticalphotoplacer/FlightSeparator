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

from os import listdir, makedirs
from os.path import isfile, join, basename, exists
import shutil
import exifread
from datetime import datetime


def getDateExif(filepath):
    """
    Extract datetime of the photo and format it.

    Parameters
    ----------
    filepath : string
        Full path to the photo.

    Returns
    -------
    date : string
        Formatted date of the photo. The format is '%Y:%m:%d %H:%M:%S'

    """

    with open(filepath, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        str_date = str(tags["EXIF DateTimeOriginal"])
        date = datetime.strptime(str_date , '%Y:%m:%d %H:%M:%S')

    return date

def getPhotos(folder, exts=('.jpg')):
    """
    Get a list of photos within the folder.

    Parameters
    ----------
    folder : string
        Full path to the folder containing photos.
    exts : tuple, optional
        Supported photo extensions. The default is ('.jpg').

    Returns
    -------
    imgs : list
        A list of photos matched with the search criteria.

    """

    folder = str(folder)

    imgs = []
    if exists(folder):
        imgs = [join(folder, f) for f in listdir(folder) if (isfile(join(folder, f)) and f.lower().endswith(exts))]

    return imgs

def clusterList(X, maxdiff):
    """
    Cluster photos into flights based on time difference

    Parameters
    ----------
    X : 2D list
        Contains photo name, date, timestamp for each photo.
    maxdiff : int
        Maximum allowable time difference between consecutive photos within the same flight.

    Returns
    -------
    result : 2D list
        Each sublist contains photos of the same flight.

    """

    X = [list(i) for i in zip(*X)]
    X.sort(key=lambda x : x[2] , reverse = False)
    X_time = [i[2] for i in X]
    breaks = list()
    seed = X_time[0]
    i = 0
    result = list()
    for i in range(0, len(X_time)):
        if (X_time[i] - seed) > maxdiff:
            result.append(breaks)
            breaks = list()
            breaks.append(X[i])
        else:
            breaks.append(X[i])
        seed = X_time[i]

    if breaks:
        result.append(breaks)

    return result

def moveFlight(flist, folder):
    """
    Move photos of the same flight to a folder.

    Parameters
    ----------
    flist : 1D list
        Contains fullpath to photos.
    folder : string
        Fullpath of the destination folder.

    Returns
    -------
    None.

    """
    if not exists(folder):
        makedirs(folder)

    for i in flist:
        outname = "{0}/{1}".format(folder, basename(i))
        shutil.move(i, outname)

def copyFlight(flist, folder):
    """
    Copy photos of the same flight to a folder.

    Parameters
    ----------
    flist : 1D list
        Contains fullpath to photos.
    folder : string
        Fullpath of the destination folder.

    Returns
    -------
    None.

    """
    if not exists(folder):
        makedirs(folder)

    for i in flist:
        outname = "{0}/{1}".format(folder, basename(i))
        shutil.copy(i, outname)

def formatResult(flights, photos):
    """
    Format the processing result of function flightSeparator to be displayed as log in the main UI.

    Parameters
    ----------
    flights : 1D list
        Contains fullpath of the flight folders which photos will be moved to.
    photos : 1D list
        Contains photo names.

    Returns
    -------
    log : string
        Formatted string as log.

    """

    log = list()
    len_s = len(flights[0])

    n_flights = len(flights)
    log.append("Number of flights detected: {0}".format(n_flights))
    for i in range(0, n_flights):
        log.append("-" * len_s)
        log.append(flights[i])
        r_ = ["{0}: {1}".format(basename(e[0]), e[1]) for e in photos[i]]
        log = log + r_

    log = "\n".join(str(x) for x in log)
    log = log + "\n"
    return log

def flightSeparator(folder, exts, fstime, iskeep, progress_callback):
    """
    Group photos into flights and move to separate folders

    Parameters
    ----------
    folder : string
        Full path to the folder containing photos.
    exts : tuple
        Supported photo extensions.
    fstime : int
        Maximum allowable time difference (in seconds) between consecutive photos within the same flight.
    iskeep: boolean
        Keep one copy of the photos in the input folder or not
    progress_callback : object
        Object to update progress to the main UI.

    Raises
    ------
    Exception
        1. No photo found in the folder -> cannot proceed.

    Returns
    -------
    dict
        Contains one element:
            - msg: log to be displayed in the main UI.

    """
    photos = getPhotos(folder, exts)

    if not photos:
        raise Exception('No photo found.')

    # first, get date and time stamps
    photo_dates = [getDateExif(i) for i in photos]
    photo_timestamps = [int(x.timestamp()) for x in photo_dates]

    # then, separate
    flights = list()
    flights.append(photos)
    flights.append(photo_dates)
    flights.append(photo_timestamps)
    flights = clusterList(flights, fstime)

    # finally, move photos into separate folders
    n_processed = 0
    n_photos = float(len(photos))
    out_folders = list()
    for i in range(0, len(flights)):
        out_folder = join("{0}".format(folder), "FL_{0}.{1}".format(str(i), datetime.fromtimestamp(int(flights[i][0][2])).strftime("%Y_%m_%d.%I_%M")))
        flist = [j[0] for j in flights[i]]
        if iskeep is True:
            copyFlight(flist, out_folder)
        else:
            moveFlight(flist, out_folder)
        out_folders.append(out_folder)

        # set progress
        n_processed = n_processed + float(len(flist))
        percent = (n_processed/n_photos) * 100
        progress_callback.emit(percent)

    log = formatResult(out_folders, flights)

    return {'msg': log}
