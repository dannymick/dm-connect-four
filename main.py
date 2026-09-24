from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

EMPTY = 0
BLUE = 1
RED = 2
ROWS = 6
COLUMNS = 7
TOTAL_CELLS = 42

Cell = Annotated[
    int,
    Field(
        strict=True,
        ge=0,
        le=2
    )
]

Row = Annotated[
    list[Cell],
    Field(
        min_length=ROWS,
        max_lenght=ROWS
    )
]

Board = Annotated[
    list[Row],
    Field(
        min_length=ROWS,
        max_length=ROWS
    )
]

def get_player_name(player):
    return "blue" if BLUE else "red"

def count_pieces(board):
    blue_count = 0
    red_count = 0

    for row in board:
        for cell in row:
            if cell == EMPTY:
                continue
            if cell == BLUE:
                blue_count += 1
            elif cell == RED:
                red_count += 1
    
    return blue_count, red_count

def get_winning_line(board, starting_row, starting_col, row_step, col_step):
    curr_player = board[starting_row][starting_col]
    cells = []
    # scan board in each direction, 4 possible moves
    for i in range(4):
        row = starting_row + (row_step * i)
        col = starting_col + (col_step * i)

        # check if in board bounds
        if row < 0 or row >= ROWS or col < 0 or col >= COLUMNS:
            return None

        if board[row][col] != curr_player:
            return None

        cells.append({
            "row": row,
            "column": col
        })
    
    return cells

def get_wins(board):
    wins = []
    for row in range(ROWS):
        for col in range(COLUMNS):
            # cell empty continue with board scan
            if board[row][col] is EMPTY:
                continue
            # scan all possible directions
            for row_step, col_step in ((0,1), (1,0), (1,1),(-1,1)):
                cells = get_winning_line(board, row, col, row_step, col_step)
                if cells is not None:
                    wins.append({
                        "player": board[row][col],
                        "cells": cells
                    })
    return wins

def check_out_of_place(board):
    for row in range(ROWS - 1):
        for col in range(COLUMNS):
            if board[row][col] != EMPTY and board[row + 1][col] == EMPTY:
                raise ValueError("Out of place")

def evaluate_board(board):
    check_out_of_place(board)
    
    blue_count, red_count = count_pieces(board)
    # handle game winner resp
    wins = get_wins(board)

    blue_winner = False
    red_winner = False

    # iterate through wins to determine game winner
    for win in wins:
        if win["player"] == BLUE:
            blue_winner = True
        else:
            red_winner = True

    if blue_winner and red_winner:
        raise ValueError("There can only be one winner")
    # handle stalemate resp
    if blue_count + red_count == TOTAL_CELLS:
        return {
            "status": "stalemate"
        }

    if len(wins) > 0:
        winner = wins[0]["player"]
        return {
            "status": "gameover",
            "winner": get_player_name(winner),
            "winning_coords": wins[0]["cells"]
        }

    # handle game in progress resp
    next_player = BLUE if blue_count == red_count else RED

    return {
        "status": "in_progress",
        "next_player_turn": get_player_name(next_player)
    }

class BoardRequest(BaseModel):
    board: Board

@app.post("/evaluate-board-state")
def evaluate_board_state(request: BoardRequest):
    try:
        return evaluate_board(request.board)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))