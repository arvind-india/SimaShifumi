# SímaProject: SHIFUMI
Our GitHub Page: [here](https://hugo-p.github.io/SimaShifumi/)

Our GitHub Project: [here](https://github.com/hugo-p/SimaShifumi/)

***

1. [Documentation](#documentation)
2. [SimaArduino](#simaarduino)
	* [Features](#features)
	* [How it works ?](#how-it-works-)
	* [Usage](#usage)
3. [SimaSHIFUMI](#simashifumi)
	* [Features](#features-1)
	* [Requirements](#requirements)
	* [Usage](#usage-1)
		* [Sources](#sources)
		* [Windows Application](#windows-application)
	* [Screenshots](#screenshots)

***

## Documentation

Part of the SimaSLI Project: [here](http://hugo.pointcheval.fr)

***

## SimaArduino

Get SimaArduino from SimaSLI! [here](https://hugo-p.github.io/SimaSLI/)

#### Features
* List of pins
* Serial communication
* Flex sensors support
* 1 finger = 6 states

#### How it works ?
It acquires the value of flex sensors and "remaps" to make a multiple of 3.
Then it tests in wich state is the finger.

#### Usage
Simply adjust the timer and your pins and it's ready to be upload on your board.

***

## SimaSHIFUMI

It's the game! Play Rock, Paper, Scissors against computer!

#### Features
* SimaCore Intergration.
* Config file
	* Shifumi: port, baudrate, score limit.
* Logger
* Cool songs !

#### Requirements
* Python 2.7~
* Modules
	* pyserial
	* pygame

`pip install pyserial`

`pip install pygame`

#### Usage

##### Sources

* Clone the repo
* Open a console in the root folder
* And launch it with

`python SHIFUMI.py`

3 modes:
* With a connected glove (With Sima technology)
* With [P] for Rock, [F] for Paper, and [C] for scissors
* Let the computer play randomly.

##### Windows Application

In dev...

#### Screenshots
Startup
![SIMASHIFUMI Startup](https://hugo-p.github.io/SimaShifumi/startup.png)
In game
![SIMASHIFUMI In game](https://hugo-p.github.io/SimaShifumi/battle.png)
Score screen
![SIMASHIFUMI Score screen](https://hugo-p.github.io/SimaShifumi/victory.png)

***
