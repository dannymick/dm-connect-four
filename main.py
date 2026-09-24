from fastapi import FastAPI

app = FastAPI()

@app.post("/evaluate-board-state")
def evaluate_board_state(request):
    pass