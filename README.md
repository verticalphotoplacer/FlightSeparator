# Flight Separator

Flight Separator tool detects and separates drone photos in a folder taken in different flights based on timestamps. 

## Usage

### Download precompiled executable for Windows

### Use as Python application

Flight Separator could be used as an Python application.
It requires <b>exifread</b> library.

### Build local executable file

<b>pyinstaller</b> is a recommended tool to build a local executable file.
It is recommended to build from a minimal Python environment. This will exclude unnecessary packages and create minimum size executable file.

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

3. Create specfile used in building the executable file

```
cd your_path/flight_separator
pyinstaller --onefile main.py
```

4. Modify spec file to include all image/ui/exe/config file into the executable

    Please refers to [main.spec](https://github.com/verticalphotoplacer/FlightSeparator/blob/master/main.spec) file.

5. Create executable

```
pyinstaller --onefile main.spec
```

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
