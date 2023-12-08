# ATDL File Reader
Reads an ATDL XML file and generates an HTML file, with details of each algo.

ATDL : Algorithmic Trading Definition Language

https://www.fixtrading.org/standards/fixatdl/

# Introduction
This is built with Python 3 and uses the [flet.dev](https://flet.dev/) library for the GUI.

# Execution
To run the script use the following commands:
```
flet ATDLtoHTML.py
```
or
```
python ATDLtoHTML.py
```
# Result

With a proper ATDL XML selected, an "output" folder will be created (only first time) in the script directory and a parsed HTML file will be placed in it.
This HTML file will have details of all the Algos present in the ATDL file in a clean tabular format.
Click on the strategy names in the generated HTML file to view the details.

# GUI
Select and upload an ATDL XML file 
![image](https://github.com/dhimanr/ATDL_File_Reader/assets/60633025/fcd136c1-f415-4600-976a-c32a374b5485)

# Example

A sample ATDL file sample_atdl.xml is attached along with the generated HTML file.

![image](https://github.com/dhimanr/ATDL_File_Reader/assets/60633025/bfb57875-a336-4917-affc-9196cd25819c)

![image](https://github.com/dhimanr/ATDL_File_Reader/assets/60633025/dbfff2b7-19e5-4058-85c7-95962ad974c5)

