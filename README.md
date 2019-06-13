# FreeCAD Builder for Monthy's CAD

This is a FreeCAD implementation for writing your Monthy's
CAD scripts. I hope you will find it useful.

## If FreeCAD alredy has a python API... why someone will use the Monty's Builder?

Writing scripts in FreeCAD could be a little bit messy. Thankfully, Monty's make
things simpler, more human readable and more natural. And also keeps the
geometry parametric (that's something that FreeCAD native scripting doesn't always do).
Nevertheless, if you're into scripting in FreeCAD there are others alternatives like
[cadquery](https://github.com/dcowden/cadquery) that may help.

## Installation

1. Install [FreeCAD](https://www.freecadweb.org/downloads.php).
2. Download this folder into your computer.
3. Now add that directory to your PYTHONPATH.

That's it boys and girls. Now you can start FreeCAD and run your scripts by
importing the library.

```python
from Monthys_FreeCAD import *

# Your code here
```

If you are interested in writing scripts in a diferent editor and then export the results
(STL, IGES, STEP), you can execute the following command in your terminal:

```
FreeCADCmd.exe your_script.py /your_directory
```

Where:
 + `FreeCADCmd.exe` is a executable that you have to find in the FreeCAD folder. You have to add that directory to your system path.
 + `your_script.py` is your script.
 + `/your_directory` is the directory where is placed `your_script.py`. If your're running the script directly in `/your_directory` you can just ommit this last argument.