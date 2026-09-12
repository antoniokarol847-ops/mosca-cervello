from fastapi import FastAPI
app = FastAPI()
import random

@app.post("/think")
def think(data: dict):
    dist = data.get("dist_to_door", 10)
    mx = (random.random()-0.5)*2
    mz = (random.random()-0.5)*2
    # se è vicino alla porta, va dritto verso la porta
    if dist < 20:
        mx = -0.2
        mz = 0.5
    return {"move_x": mx, "move_z": mz, "spikes": random.randint(0,10), "action": "cammina"}
