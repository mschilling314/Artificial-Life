# Artificial-Life

For the current version of the main branch (merged from Evolving-Bodies-V3), I added onto Ludobots.  

# Project

## Description
In this project, I worked to build the ability to evolve bodies and brains for the simple task of locomotion in one direction.  I built on top of Ludobots, which you can find in the citations.


## Generation of Bodies
To generate bodies, I utilized the same indirect encoding as Karl Sims in his paper (see citations).
![Genotype to Phenotype](diagrams/Morphology.PNG)

Above is a diagram that shows an example of this, with the directed graph on the left forming, as an example, the figure on the right, where the green blocks have sensors and the blue don't.


## Generation of the Brain
The brain is generated by first randomly assigning sensor neurons to some links, and assigning motor neurons to all links.  There's a hidden layer in between, and the network is fully connected.
![Brain](diagrams/NeuralNet.PNG)

Above is one example of a possible brain.

## Mutation
![Mutation](diagrams/Mutation.PNG)

The graph above shows the probability of given mutations.  Worth noting is that I made the probability of any mutations to the body lower, both because I believe that in biological creatures it's harder to change your body than brain, and also because it saves compute time since whenever the body evolves, you have to go back through its generation procedure.

Note that similar to actual evolution, multiple evolutions can happen.  Though this chart shows things as more of a flow, I did that simply so that it is more apparent what the possibilities are.  In actuality, any of these evolutions can happen in a given mutation cycle.


## Selection
To select for the robots that should be evolved further, we used a parallel hill climber methodology wherein we have some population, which we then clone and mutate, and within each "silo" of parent/child pairs, we select the one with the better fitness (higher x-value in this case) to be the one that continues evolving.

## Running It
Once you've installed the prerequisites (there are a lot, sorry), you can then do a few things.  The first option is to simply run main.py.  Doing this will provide you with the option to either run evolution from scratch, or see some of the best runs that I made.

## Some Results
Below are two graphs containing parent and child fitness values.
![ParentFitness](diagrams/ParentFitness.PNG)
![ChildFitness](diagrams/ChildFitness.PNG)

Weirdly, it seems like the parent doesn't increase in fitness monotonically as it should.

Though the professor wanted 50,000 simulations, I was only able to run about 2,500 both because my computer is rather weak (it died multiple times trying to handle the load), I also didn't have much time on my hands as I wound up behind and was unable to catch up until recently (today).  Though, I did calculate that the time to run 50,000 simulations on my computer would be approximately 16 hours and 40 minutes.  Of course, this was with a slightly different configuration than the professor had requested, namely, I was thinking along the lines of a population size of 25 with 2000 generations of evolution, rather than 10 random seeds with 10 as the population size and 500 generations.  Regardless, this came from noticing that it took an hour to run 3,000 simulations, which equates to roughly 0.005 minutes per simulation, which when multiplied by 50,000 gives the projected time.

However, given that I did not have any truly large blocks of time with which my system could run simulations (it can either run simulations or do other things, it's literally not strong enough to do simulations and anything else) since I had to pull so many near all-nighters to do work for other classes as well as try to get this code working, my simulation count obviously fell short.


## A 10-Second Teaser

<iframe width="560" height="315" src="https://www.youtube.com/embed/wbDy_aavwSc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

It's worth noting that there's no free software I could find that can capture a screen recording on Windows, XBox didn't quite cut it as that requires you to select the window, and the simulation was opening and closing windows.

## 2-Minute Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/p1p2iBilarY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

It's worth noting that there's no free software I could find that can capture a screen recording on Windows, XBox didn't quite cut it as that requires you to select the window, and the simulation was opening and closing windows.

# Citations
Karl Sim's Paper on evolution in a digital environment, found [here](https://www.karlsims.com/papers/alife94.pdf)

This project built upon the Ludobots course, which can be found [here](https://www.reddit.com/r/ludobots/).

The class this project came from is listed as Computer Science 396 at Northwestern University, the section is Artificial Life taught by Sam Kriegman.  The syllabus for the class can be found [here](https://docs.google.com/document/d/1jURIbvpQ0imcaMk-AHUmj_szZNtsA4lZAlcqXa6usXs/edit).
