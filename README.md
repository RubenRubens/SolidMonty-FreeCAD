# FreeCAD Builder for SolidMonty

This is a FreeCAD implementation for writing your SolidMonty
CAD scripts. I hope you will find it useful.

## If FreeCAD alredy has a python API... why someone will use the SolidMonty Builder?

Writing scripts in FreeCAD could be a little bit messy. Thankfully, SolidMonty make
things simpler, more human readable and natural.
Nevertheless, if you're into scripting in FreeCAD there are others alternatives like
[cadquery](https://github.com/dcowden/cadquery) that may help.

## Installation

1. Install [FreeCAD](https://www.freecadweb.org/downloads.php).
2. Download [this folder](https://github.com/RubenRubens/SolidMonty-FreeCAD/FreeCAD_Builder_for_SolidMonty) into your computer.
3. Now add that directory to your PYTHONPATH.

That's it boys and girls. Now you can start FreeCAD and run your scripts by
importing the library.

```python
from SolidMonty_FreeCAD import *

# Your code here
```

## How to run the FreeCAD Builder for Solid Monty in the terminal?

If you are interested in writing scripts in a diferent editor and then export the results
(STL, IGES, STEP), you can execute the following command in your terminal:

```
FreeCADCmd.exe your_directory/your_script.py
```

Where:
 + `FreeCADCmd.exe` is a executable that you have to find in the FreeCAD folder. You have to add that directory to your system path.
 + `your_script.py` is your script.
 + `your_directory` is the directory where is placed `your_script.py`. If you're running the script directly in the current working directory it is not neceary to write it.
