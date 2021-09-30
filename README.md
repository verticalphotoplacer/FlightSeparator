# Flight Separator

Flight Separator tool detects and separates drone photos in a folder taken in different flights based on timestamps. 

## Installation

There are three ways to install this tool: use a [precompiled executable](#use-precompiled-executable-for-windows), run as [Python application](#use-as-python-application) or [build local executable file](#build-local-executable-file).

### Use precompiled executable for Windows

A precompiled executable is provided at [the bin directory](https://github.com/verticalphotoplacer/FlightSeparator/tree/master/bin).
Please download to your computer and double-click to run.

### Use as Python application

Flight Separator could be used as a Python application.
It requires <b>exifread</b> library.

```
pip install exifread
```

Then, navigate to your local flight_separator directory and run main.py

```
cd your_path/flight_separator
python main.py
```

### Build local executable file

[pyinstaller](https://www.pyinstaller.org/) is a recommended tool to build a local executable file.
It is recommended to build from a minimal Python environment. This will exclude unnecessary packages and create a minimum size executable file.

1. Create and activate a virtual environment in your [Python installation](https://www.python.org/downloads/).

```
mkdir py36envtest
python -m venv venv_py36
venv_py36\Scripts>activate.bat
```

2. Install dependencies

```
pip install exifread
```

3. Install pyinstaller

```
pip install pyinstaller
```

4. Download the source code of Flight Separator to your local machine

git clone https://github.com/verticalphotoplacer/FlightSeparator.git
cd HeadingCalculator

4. Modify spec file to include all image/ui/exe/config file into the executable

```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'main.ui', '.' ),
         ( 'icon/app.png', 'icon/' ),
		 ( 'icon/copypaste.png', 'icon/' ),
		 ( 'icon/erase.png', 'icon/' ),
		 ( 'icon/save2file.png', 'icon/' ),
         ]

a = Analysis(['main.py'],
             pathex=['your_path_to_FlightSeparator_folder'],   # change this line
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
```

5. Create executable

```
pyinstaller --onefile main.spec
```


## Usage

Please follow the steps in Figure 1. The result is shown in the log.
A folder is created for each detected flight, to store the flight's photos. 

<p align="center">
  <img align="middle" src="https://github.com/verticalphotoplacer/FlightSeparator/blob/master/docs/img/fl_howtouse.PNG?raw=true" alt="Flight Separator usage">
  <br>
  <br>
  <em><b>Figure 1. Using Flight Separator</b></em>
</p>

Input folder before (Figure 2) and after running the tool (Figure 3). In this example, there are photos from 3 different flights in the input folder.

<p align="center">
  <img align="middle" src="https://github.com/verticalphotoplacer/FlightSeparator/blob/master/docs/img/original_folder.PNG?raw=true" alt="Input folder before">
  <br>
  <br>
  <em><b>Figure 2. Input folder before running Flight Separator</b></em>
</p>

<p align="center">
  <img align="middle" src="https://github.com/verticalphotoplacer/FlightSeparator/blob/master/docs/img/ran_folder.PNG" alt="Input folder after">
  <br>
  <br>
  <em><b>Figure 3. Input folder after running Flight Separator</b></em>
</p>

This tool could be used to support [Vertical Photo Placer](https://verticalphotoplacer.github.io/VerticalPhotoPlacer/) which may require same-flight photos in some of its features.

## Contributing

If you find some issue that you are willing to fix, code contributions are welcome. 

## Author

* **Man Duc Chuc** 

## Credits

The author thanks the International Digital Earth Applied Science Research Center, Chubu University and National Research Institute for Earth Science and Disaster Resilience (NIED), Japan.

## License

This software is distributed under a GNU General Public License version 3.

## How to cite 
Coming soon!

## Related tools
* [Heading Calculator](https://github.com/verticalphotoplacer/HeadingCalculator)
* [Vertical Photo Placer Plugin](https://github.com/verticalphotoplacer/VerticalPhotoPlacer)
