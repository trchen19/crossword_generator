# Automated Crossword Puzzle Generator

This project implements an automated solution generator based on artifical intelligence heuristic search methods to solve the Crossword Constraint Satisfaction Problem. The word search component of this automated generator is supported by a MySQL database populated with words and clues that were from various American Crossword Puzzles. Beyond the crossword solution generator, this system also includes infrastructure to manipulate heurstic search and grid constraints and to run experiments on an arbitraily large number of randomly generated grids. Moreover, this system also includes a GUI that allows for users to generate individual puzzles and complete them. The system defaults to the GUI for general usability, but tests results of an experiment I ran can be found within the "testing" directory. 

## Getting Started
Follow these instructions to run this crossword generator on your local system. 

### Prerequisites

##### Packages and Installation

Run in the base directory:

```pip install -r requirements.txt```


MySQL Database:

Follow instructions to download a free MySQL database at https://www.mysql.com/downloads/.
This project requires that you have a MySQL Databse. 

#### Connecting to your MySQL Database and Populating
To connect your database to this system, input your database name, user, and password in the respective variables at the beginning of UpdateBoard.py and PopulateDB.py. 

After changing your login info, populate your database with the crossword terms and clues by running:

```python populateDB.py```

### Launching the Generator

Simply run:

```python boardgui.py```

## Notes about Experimentation Infrastructure
The infrastructure for running experiments currently is not linked with the generation system. Connecting the two requires detaching the backend system from the GUI and calling the helper functions in inputGenerator.py. Documentation for experiments that I ran on this system are contained in Crossword_Generation_Experiment_Report.pdf in the testing directory. 

## Acknowledgments

Resources used in this implementation:

* G. Meehan and P. Gray. Constructing Crossword Grids: Use of Heuristics vs. Constraints 
* D. Cheng and N. Dhulekar. Crossword Puzzle Generator. 