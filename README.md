# Artificial-Life

For the current version of the main branch (merged from Person), I added onto Ludobots.  The Person Branch was created from the Quadrupeds Branch, which is the last
part covered by Ludobots.  Person has a few changes.  First off, I switched the morphology to that of a biped with feet.  Second, I added a hidden layer with five
neurons.  Third, I came up with a way to procedurally generate a brain based off of a solution's body.  It is my hope that in the future I can figure out a way to
procedurally generate the body too, but when I tried this it went poorly to say the least.

# Assignment 7
## Overview
In this assignment, I modified solution.py among other files so that I could procedurally generate 3-D morphologies with some randomness.  These changes can be seen in the branch 3D-Body-Gen.  Right now, running main.py will rapidly generate a sequence of creatures as specified in the Generation section, with randomly assigned sensor neurons for the individual links, which are green if there is a sensor present, blue otherwise.

## Generation

## Codebase

The following diagram illustrates most of the codebase's structure, courtesy of Professor Kriegman (see citations below).
<img Title="Overarching Structure of Codebase" alt="Codebase Diagram" src="diagrams/ludobots.png"></img>
Though, instead of evolve.py, we use search.py which makes calls to parallelHillClimber.py to actually do the evolution, where each call to solution.py within parallelHillClimber.py is equivalent to the genome blocks.

## Video Demonstration


# Citations
This project built upon the Ludobots course, which can be found [here](https://www.reddit.com/r/ludobots/).

The class this project came from is listed as Computer Science 396 at Northwestern University, the section is Artificial Life taught by Sam Kriegman.  The syllabus for the class can be found [here](https://docs.google.com/document/d/1jURIbvpQ0imcaMk-AHUmj_szZNtsA4lZAlcqXa6usXs/edit).
