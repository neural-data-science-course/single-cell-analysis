[//]: # (You can remove theses instructions when you have setup the first version of the module)

## Module template instructions
This is the template for creating a new module in the 'neural data science course'.

### What is a module?
A module is a set of lessons revolving around a central topic. 
The core of each lesson is a jupyter notebook with both working code and explanations.
See https://github.com/neural-data-science-course/population-methods for an example.

### How to use this template to create a new module?
  1. Create a new Github repository by clicking the green 'Use this template' button on the top right.
  2. Create the repository in the neural-data-science-course organisation and give it a title [number]-[module name].
  3. Submit a pull request that adds a link to the new module to the course website https://github.com/neural-data-science-course/neural-data-science-course.github.io.

### What changes should I make to this README?
  - [ ] Change the title
  - [ ] Add a module introduction, introducing the main overarching topic and what a student will learn in the module.
  - [ ] Adapt the module overview, include how long it takes to teach each lesson in the module.
  - [ ] Add prerequisites
  - [ ] Adapt setup instructions if necessary
  - [ ] Add details about the contributors of this module
  - [ ] If you want, add how this module should be cited
  - [ ] Remove (or comment out) these instructions
 
### How to create my first lesson?
   - [ ] Use the `01-lesson1` folder as an example
   - [ ] Adapt the `lesson-title.ipynb`, this should be the main explanatory resource used for teaching.
      1. Try to stick to the template as much as possible, so all lessons in the course have a similar look and feel.
      2. Try to fill the 'In this lesson you will learn' on top and 'Keypoints' in the bottom of the notebook as well as possible. 
         This will provide a natural intro and ending to the notebook and gives a lot of structure to the course.
   - [ ] Adapt the `exercises.ipynb`, you can add separate exercises without answers here, these can be used for assignments.
   - [ ] If necessary add code you use in the notebook in the `code` folder
   - [ ] To add more lessons, just add more folders with a similar structure

### What other changes should I make?
   - [ ] Update the `instructor-notes.md` file with instructions for the instructor teaching this module.
   - [ ] Update the `requirements.txt` file with python packages necessary for this module.
----

# Module [number]: [module name] 
Welcome to module [number] of the [Neural Data Science Course]().
[Module introduction]

## Prerequisites
To make the best out of the material of this module, you will need:  
*

## Setup

### Install Pyhton and anaconda on your machine 
If you don't have them already installed, install Pyhton and Anaconda on your machine.
Follow these instructions on [how to install anaconda](https://docs.anaconda.com/anaconda/install/)

### Create a conda environment**
Create a conda virtual environment with the name you prefer, then activate it to work within it.
Open a terminal, or open 'Anaconda Prompt' from Anaconda Navigator, in there run:

```
conda create --name env_name
conda activate env_name
```


### Download the module folder
Clic on Code/Download Zip at the top of the page.  
Move the zipped folder in the directory of your choice and decompress it.  
Open the terminal and navigate to the module directory.

### Install the module requirements

Run in the terminal

```
pip install -r requirements.txt
```

### Open Jupyter lab
You can now open the lesson's notebooks in jupyter lab
```
jupyter lab
```

### All set!
You're all set to go through the lessons.

## Module overview
* 01. [lesson name] - [XX] minutes
* 02. [lesson name] - [XX] minutes


## Contributors
This module was created by:  
* contributor 1  
* contributor 2  

## License


Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

## Citation
If you want to cite this module, please use:
