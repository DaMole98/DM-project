# DM-project
Project of the Data Mining course

## Project description

The project description is available in the file `DM_project.pdf`.

## Data

The data is available in the folder `data`.

## Code

The code is available in the folder `src`.

## Project structure

The project structure is the following:

```
.
|-- .gitattributes
|-- .gitignore
|-- checks.json
|-- DM_Project_23-24.pdf
|-- README.md
|-- tree_structure.txt
|
|-- .idea
| |-- .gitignore
| |-- DM-project.iml
| |-- misc.xml
| |-- modules.xml
| |-- vcs.xml
| |-- workspace.xml
| |
| |-- inspectionProfiles
| | |-- profiles_settings.xml
| | |-- Project_Default.xml
| |
| ??? shelf
| |-- Uncommitted_changes_before_Checkout_at_12_01_2024_00_04__Changes_.xml
| |-- Uncommitted_changes_before_rebase__Changes_.xml
| |-- Uncommitted_changes_before_rebase__Changes_1.xml
| |-- Uncommitted_changes_before_rebase__Changes_2.xml
| |-- ...
|
|-- build
| |-- clang_tidy
|
|-- data
| |-- dev_data
| | |-- cities.json
| | |-- drivers.json
| | |-- drivers_prefs.json
| | |-- items.json
| |
| |-- medium1_dataset
| | |-- actual.json
| | |-- HiddenRoutes.json
| | |-- parameters.json
| | |-- standard.json
| |
| |-- medium_dataset
| | |-- actual.json
| | |-- HiddenRoutes.json
| | |-- parameters.json
| | |-- standard.json
| | |-- ...
| |
| ??? small_dataset
| |-- actual.json
| |-- HiddenRoutes.json
| |-- parameters.json
| |-- standard.json
|
|-- src
| |-- Class_Structures
| | |-- ClassesDefinition.py
| | |
| |-- Data_Generator
| | |-- actual_route_generator.py
| | |-- hidden_route_generator.py
| | |-- input_dataset_generator.py
| | |-- ...
| |
| |-- Solver_Programs
| | |-- dist-with-marius2-dist.png
| | |-- dist.png
| | |-- DistanceMetrics.py
| | |-- GAStdGen.py
| | |-- HiddenRouteFinder.py
| | |-- MainSolver.py
| | |-- ...
| |
| |-- Testers
| |-- DistanceTester.py
| |-- ...
``` 

## How to run the code

To run the code, you need to run the file `main.py` in the folder `src`. The code is written in Python 3.9. The required packages are listed in the file `requirements.txt`. To install them, you can run the following command:
if you are using pip:
```
pip install -r requirements.txt
```
if you are using conda:
```
conda install --file requirements.txt
```

The code has been developed and tested on pyCharm Community Edition 2020.3.2. it is recommended to use the same IDE to run the code. Running the code in other IDEs or in the terminal may cause some errors, in particular in the visualization part and importing the modules.
The interpreter used is Python 3.9.1. To change the interpreter, go to `File -> Settings -> Project: DM-project -> Python Interpreter` and select the interpreter you want to use.