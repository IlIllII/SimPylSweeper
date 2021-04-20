# -*- coding: utf-8 -*-
"""
Logic module containing the underlying game logic needed to play minesweeper.
Users can play minesweeper with the interpreter by using the functions
contained herein.
"""


def print_board(game: dict) -> None:
    """Print a readable version of the game."""
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def _new_board(num_rows: int, num_cols: int, bombs: list) -> tuple:
    """Create a board with bombs and a mask that is all False."""
    board = []
    mask = []
    for r in range(num_rows):
        row_b = []
        row_m = []
        for c in range(num_cols):
            row_m.append(False)
            if [r, c] in bombs or (r, c) in bombs:
                row_b.append(".")
            else:
                row_b.append(0)
        board.append(row_b)
        mask.append(row_m)
    return board, mask


def _populate_numbers(board: dict, num_rows: int, num_cols: int) -> dict:
    """Populate numbers on board based on quantity of proximal bombs."""
    # Iterate over board using a 3x3 kernel to assign bomb numbers to tiles.
    for r in range(num_rows):
        for c in range(num_cols):
            bombs = 0
            for row in range(max(0, r - 1), min(num_rows, r + 2)):
                for col in range(max(0, c - 1), min(num_cols, c + 2)):
                    if board[row][col] == ".":
                        bombs += 1
            board[r][c] = bombs if not board[r][c] == "." else "."
    return board


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters
    ----------
    num_rows : int
        Number of rows on board.
    num_cols : int
        Number of columns on board.
    bombs : list[tuples]
        List of bomb coordinates (row, column).

    Returns
    -------
    game : dict
        A dictionary containing dimensions, board, mask, and state keys.


    >>> print_board(new_game_2d(3, 3, [(1,1)]))
    board:
        [1, 1, 1]
        [1, '.', 1]
        [1, 1, 1]
    dimensions: (3, 3)
    mask:
        [False, False, False]
        [False, False, False]
        [False, False, False]
    state: ongoing
    """
    board, mask = _new_board(num_rows, num_cols, bombs)
    board = _populate_numbers(board, num_rows, num_cols)

    game = {
        "dimensions": (num_rows, num_cols),
        "board": board,
        "mask": mask,
        "state": "ongoing",
    }

    return game


def _dig_2d_recur(game, row, col):
    """Recursively dig up tiles. Return number of tiles dug up."""
    mask = game["mask"]
    num_rows, num_cols = game["dimensions"]
    tile = game["board"][row][col]
    mask[row][col] = True

    if tile == ".":
        game["state"] = "defeat"
        return 0
    elif tile > 0:
        return 1
    else:
        # Use 3x3 kernel to recursively dig up nearby tiles.
        total = 1
        for r in range(max(0, row - 1), min(num_rows, row + 2)):
            for c in range(max(0, col - 1), min(num_cols, col + 2)):
                if mask[r][c] is False:  # If tile is hidden, dig up.
                    total += _dig_2d_recur(game, r, c)
        return total


def dig_2d(game: dict, row: int, col: int) -> int:
    """
    Dig up tile. If blank, recursively dig up surrounding tiles.

    Updates game['board'] and game['mask'] for given coordinate. If blank,
    recursively digs up surrounding tiles. If tile contains a number, return 1.
    If the tile contains a bomb, change game state to defeat and return.

    Before returning, loops over game board and see if the player has won.
    If so, function mutates the game['state'] before returning.

    Parameters
    ----------
    game : dict
        Dictionary of the game containing dimensions, state, board, and mask.
    row : int
        Row index.
    col : int
        Column index.

    Returns
    -------
    num_revealed : int
        Total number of tiles dug up by the function.

    """
    num_revealed = _dig_2d_recur(game, row, col)
    if game["state"] == "defeat":
        return num_revealed
    covered = 0
    for i, r in enumerate(game["mask"]):
        for j, c in enumerate(r):
            if c is False and game["board"][i][j] != ".":
                covered += 1
    if covered <= 0:
        game["state"] = "victory"
    return num_revealed


def render_2d(game: dict, xray: bool = False) -> list:
    """
    Create a string representation of the board.

    Makes a list of lists, representing a 2d matrix, of strings corresponding
    to the tile values of the game['board']. '.' denotes a bomb, '_' denotes
    a hidden tile, ' ' denotes an empty revealed tile, and then number strings
    are for revealed tiles with numbers.

    Parameters
    ----------
    game : dict
        A game dictionary containing dimensions, game, state, and mask keys.
    xray : bool, optional
        Option to reveal all hidden tiles. The default is False and thus only
        the tiles allowed by game['mask'] are revealed, the rest are '_'.

    Returns
    -------
    render : list
        A list of lists of strings representing the game board that is more
        fit to print.

    """
    render = []
    for i in range(len(game["mask"])):  # Iterate over the rows.
        row = []
        for j in range(len(game["mask"][i])):  # Iterate over columns
            if game["mask"][i][j] is False and xray is False:
                row.append("_")  # Hidden tile
            else:
                tile = game["board"][i][j]
                if tile == 0:
                    row.append(" ")  # Empty tile
                else:
                    row.append(str(tile))
        render.append(row)
    return render


def render_ascii(game, xray=False):
    """
    Create an ascii string of the 2d render so the board can be printed.

    Essentially joins the render_2d list of the game into a string separated
    by newlines for each row.

    Parameters
    ----------
    game : dict
        A game dictionary containing dimensions, game, state, and mask keys.
    xray : bool, optional
        Option to reveal all hidden tiles. The default is False and thus only
        the tiles allowed by game['mask'] are revealed.

    Returns
    -------
    ascii_render : str
        String representation of the game board. Tiles are represented by
        ascii characters and newlines are created for each row.

    Example:
        >>> print(render_ascii(game))
        _21 _
        _.___

    """
    render = render_2d(game, xray)
    rows = []
    for row in render:
        rows.append("".join(row))
    ascii_render = "\n".join(rows)
    return ascii_render
