# -*- coding: utf-8 -*-
"""
Provides a GUI so users can play minesweeper with a mouse.
"""

import random
from collections import namedtuple
import PySimpleGUI as sg
import logic

MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 35
DEFAULT_BOARD_SIZE = 15
BOMB_COEFF = 0.05  # Used to populate bombs based on board size


def play():
    """
    Open Minesweeper main menu.

    Returns
    -------
    None.

    """
    # Create menu window
    board_size = [
        sg.Text(text="Board Size"),
        sg.Slider(
            range=(MIN_BOARD_SIZE, MAX_BOARD_SIZE),
            default_value=DEFAULT_BOARD_SIZE,
            orientation="horizontal",
        ),
    ]

    easy = sg.Radio("Easy", "difficulty")
    medium = sg.Radio("Medium", "difficulty", default=True)
    hard = sg.Radio("Hard", "difficulty")
    extreme = sg.Radio("Extreme", "difficulty")

    layout = [
        [sg.Text("Welcome to Minesweeper!", justification="center")],  # Row 1
        board_size,  # Row 2
        [easy, medium, hard, extreme],  # Row 3
        [sg.Button("New Game"), sg.Button("Quit")],  # Row 4
    ]

    window = sg.Window("MineSweeper", layout)

    # Execute read loop
    settings = namedtuple("settings", "board_size easy medium hard extreme")
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Quit":
            break
        else:
            # Collect user inputs as game parameters and play the game.
            user_input = settings(*values.values())
            size = user_input.board_size
            total_tiles = size ** 2
            difficulties = [
                user_input.easy,
                user_input.medium,
                user_input.hard,
                user_input.extreme,
            ]

            # Adjust bomb count based on which difficulty level was selected
            for i, boolean in enumerate(difficulties):
                if boolean:
                    bombs = round((total_tiles) * BOMB_COEFF + total_tiles * (i / 20))

            new_game(size, bombs)

    window.close()


def new_game(size, bombs):
    """
    Start a new game according to user defined settings.

    Parameters
    ----------
    size : int or float
        Dimensions of square grid, eg. 9 -> 9x9 grid.
    bombs : int or float
        The number of bombs to populate the game with.

    Returns
    -------
    None. Instead, play game in GUI window.

    """
    # Randomize color scheme for extra pizazz.
    color_scheme = random.choice(list(sg.LOOK_AND_FEEL_TABLE.keys()))
    sg.change_look_and_feel(color_scheme)

    # Invert button color scheme. To be used for revealed tiles.
    revealed_tile_colors = tuple(
        reversed(sg.LOOK_AND_FEEL_TABLE[color_scheme]["BUTTON"])
    )

    # Convert floats to ints.
    size, bombs = int(size), int(bombs)

    # Permute all possible bomb locations and randomly select some subset.
    potential_bombs = [(x, y) for x in range(size) for y in range(size)]
    final_bombs = []
    while len(final_bombs) < bombs:
        final_bombs.append(
            potential_bombs.pop(random.randint(0, len(potential_bombs) - 1))
        )

    # Create a new game dict with bomb locations.
    # render_2d() creates an ascii game mask based on the game dict.
    game = logic.new_game_2d(size, size, final_bombs)
    render = logic.render_2d(game)
    layout = _create_layout(size, bombs)
    window = sg.Window("Game", layout, element_padding=(0, 0))

    # Execute game loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # Dig up clicked tile and re-render the board.
        logic.dig_2d(game, *event)  # event is (row, col) of button pressed
        render = logic.render_2d(game)

        # Loop over the rendered game mask, updating buttons as we go.
        for x in range(size):
            for y in range(size):
                render_tile = render[x][y]
                button_idx = (x, y)
                button = window[button_idx]

                # Underscore denotes that the tile is still hidden.
                if render_tile != "_":
                    button.Update(
                        text=render_tile,
                        button_color=revealed_tile_colors,
                        disabled=True,
                        disabled_button_color=revealed_tile_colors,
                    )
        window.refresh()

        # Game ending
        if game["state"] == "victory":
            sg.popup("Congrats! You win!",)
            break
        elif game["state"] == "defeat":
            sg.popup("You lose!")
            break

    window.close()


def _create_layout(size, bombs):
    """Create window layout for the game."""
    toolbar = [[sg.Text(f"Bombs: {bombs}")]]  # Display number of bombs at top.
    layout = [[sg.Column(toolbar)]]

    # Add a button grid to the layout.
    for x in range(size):
        row = []
        for y in range(size):
            widget = sg.Button(button_text="", key=(x, y), size=(2, 1))
            row.append(widget)
        layout.append(row)

    return layout
