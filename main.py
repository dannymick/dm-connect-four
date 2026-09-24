from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

EMPTY = 0
BLUE = 1
RED = 2
ROWS = 6
COLUMNS = 7

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

def evaluate_board(board):
    blue_count, red_count = count_pieces(board)
    print(blue_count, red_count)
    # handle game winner resp
    # handle stalemate resp
    if blue_count + red_count == 42:
        return {
            "status": "stalemate"
        }
    # handle game in progress resp
    return {
        "status": "in_progress"
    }

class BoardRequest(BaseModel):
    board: Board

@app.post("/evaluate-board-state")
def evaluate_board_state(request: BoardRequest):
    try:
        return evaluate_board(request.board)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))