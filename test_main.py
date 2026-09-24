from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validation_error():
    resp = client.post(
        "/evaluate-board-state",
        json={
            "board": [[]]
        }
    )

    assert resp.status_code == 422

def test_game_in_progress():
    resp = client.post(
        "/evaluate-board-state",
        json={
            "board": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 2, 1, 1, 0],
                [0, 0, 0, 1, 1, 2, 0]
            ]
        }
    )

    assert resp.status_code == 200