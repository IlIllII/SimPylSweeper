# SimPylSweeper
**Minesweeper in Python with PySimpleGUI.**

To play the game, run `main.py` in the approprite directory.

```console
python main.py
```

After running the script, the main menu should pop up:

![minesweeper_menu](https://user-images.githubusercontent.com/78166995/115398955-ab4c7800-a1b5-11eb-913c-145af3dc6af6.PNG)

You can start a new game by pressing the `New Game` button.

![minesweeper_game_board](https://user-images.githubusercontent.com/78166995/115399073-d0d98180-a1b5-11eb-9c8a-569ddd8695b8.PNG)

And then start digging! Try to avoid bombs.

***

## Current Features

* Color randomization: The color scheme is randomized each time you play by selecting new colors from over 150 visually appealing color schemes. This makes new games fresh and exciting!

![minesweeper_color_randomization1](https://user-images.githubusercontent.com/78166995/115399890-a5a36200-a1b6-11eb-8879-c9be79c6ed23.PNG)
![minesweeper_color_randomization2](https://user-images.githubusercontent.com/78166995/115399898-a76d2580-a1b6-11eb-82b6-e28e62b934b5.PNG)
![minesweeper_color_randomization3](https://user-images.githubusercontent.com/78166995/115399905-a89e5280-a1b6-11eb-817d-77a9b0b83e98.PNG)
![minesweeper_color_randomization4](https://user-images.githubusercontent.com/78166995/115399908-a936e900-a1b6-11eb-8ba2-08a83108967b.PNG)

* Difficulty Gradient: You can select between 4 different difficulties and a variable board size. This offers a diverse playerbase a fun and enriching experience, regardless of skill level. For a real challenge, try a board size of 35 and extreme difficulty!

![minesweeper_big_board](https://user-images.githubusercontent.com/78166995/115400188-fb780a00-a1b6-11eb-8e0b-21452e5b4b61.PNG)

***

## Project Architecture

This small project doesn't need too much of an explanation, but as a starting point: the `logic.py` module contains the underlying minesweeper game logic. It is playable by itself in the interpreter, but is much more fun with the GUI. The `gui.py` module contains code to run the GUI and game loop. It is implemented using PySimpleGUI. Finally, the main.py script is simply a script that plays the game.

***

## Contributing

These are a number of enhancements that I may make in the future.

**New Features**:

1. A score system based on time and number of bombs, perhaps.
2. A local leaderboard that tracks your top 10 high scores.
3. Marking hidden tiles as bombs with right click.
4. Bomb images instead of '.'.
5. Global bomb reveal at game end.
6. 3 dimensional minesweeper. Would require redoing the logic to generalize to higher dimensions.

**Other Enhancements**:

1. Integrate logic.py and gui.py better, because there is some redundancy in computation, especially in updating the board.
2. Speed up algorithms. Not a huge issue most of the time, but if you do massive boards the game can get less responsive.

**Happy Mining!**
