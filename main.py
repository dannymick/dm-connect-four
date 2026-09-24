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

def evaluate_board(board):
    pass

class BoardRequest(BaseModel):
    board: Board

@app.post("/evaluate-board-state")
def evaluate_board_state(request: BoardRequest):
    try:
        print(request)
        return evaluate_board(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))