## Protect Our Planet ( POP )

### Plot and Synopsis

There has been an attack on a rainforest by poachers. For thier own good, they selfishly :
* Cut down trees
* Hunt down animals

To protect our beloved nature, natives take action. Their objective is to prevent the total health of the ecological system from degrading too much. They are provided with weapons, just like their counterparts, to attack and hence inhibit the actions of the latter.

The battleground (with just 4 members!) is on a 6 X 6 board, with hexagonal cells.
The cells are given a `(x, y)` coordinate value with vertical rows and horizontal columns. A preview of the empty board is given below :

![board_image]( ./empty_board.png)

The user plays as a **native**, and has a clear motive to minimize the degradation of health of the environment. If all the *poachers* die, or a maximum number of turns have alreay been made, the game ends and the player wins. A defeat for the player is iminent when the health has decreased below he safe margin before the maximum number of turns is reached.

### Tools Used

The game has been implemented purely in python2. The logic and AI has been implemented in `pop.py`. The user interface has been implemented in `pygame`, which resides in file `pop_ui.py`. For proper execution of the game, python, with its minimal packages, and pygame has to be installed in the system.

### Controls
The only controls used for user interaction with the game environment is mouse click. A `left mouse click` on a hex cell is interpreted as one of the `hot cells`. The first hot cell is the `starting position`, the second is the `target position`. A start-end pair is taken as an input from the user at every turn, and an attempt to play this move is made.

### Brief Game Rules

1.  The mobile characters in our game world can move in any of the six directions corresponding to the six sides of the hexagonal tiles and one step at once.

2.  Poachers can attack every other character namely trees, animals, natives.

3.  Natives can attack poachers and animals, trees (when there's no other choice).

4.  Animals can attack both poachers and natives.

5.  Health points of a character indicate amount of life(health) left in the character.

6.  Initial health points of the characters are : Poachers (100) , Animal (45), Native(50), Tree(30).

7.  Hit points indicate the amount of loss of health points of the prey during an attack event.

8.  Hit points when animal is the attacker and prey is native is 15, when prey is poacher is 25.

9.  Hit points when poacher is the attacker and prey is native is 15, when prey is tree is 15, when prey is animal is 20.

10. Hit points when native is the attacker and prey is poacher is 10, when prey is tree is 30, when prey is animal is 50.

11. No attacker can attack their prey from a distance more than distance two hexagonal tiles.

12. Animals can attack their prey only when it is one hexagonal tile away.

### AI Implementaion
- To do

### Character Placement

### Character Movement

### Character Animantion
