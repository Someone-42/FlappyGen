# FlappyGen
First year computer science high school project

InGame screenshot example :
![ExampleImage](/assets/ExampleImage.png?raw=true "InGame example")

### Project guidelines :
- Had to be done in python
- Had to use graphics.py (Based on pygame) for rendering
- Groups of 2 people

## Requirements :
- At least Python 3.7
- Pygame

> When launching the game, make sure the current working directory is the one Main.py and SnakeEngine2.py are located

## The project :
Together with a classmate, we decided to make a simple AI game, so we based our AIs on the game "Flappy Bird"
where the point is to jump in between pipes while they scroll towards you.

When starting the game, we spawn many different birds, with each a different AI.
The AIs are 4 neurons each, where they learn how to play the game using a genetic algorithm (Automatic learning for neural networks)
-> The moment every bird has died, each AI's score is collected, we gather the 10% best and mutate their neuron weights, then spawn the same amount in the next phase.
-> Score is calculated based on the amount of time survived, and how close the bird was to the gap right before dying.

We also decided to use SnakeEngine2 which is a side project i had made earlier, a kind of "Game engine" in python. It allows us to create scenes, game objects, game models, UI elements, etc... and let the engine manage those tasks. I wanted to implement other features, like another renderer than graphics.py, like tkinter or pyopengl, but i didn't have time to implement this and then switched on to other things.

This project will not be updated. Neither will SnakeEngine2.
