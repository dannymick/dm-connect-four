from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from game_utils import Board, evaluate_board

app = FastAPI()

class BoardRequest(BaseModel):
    board: Board

@app.post("/evaluate_board_state")
def evaluate_board_state(request: BoardRequest):
    try:
        return evaluate_board(request.board)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))