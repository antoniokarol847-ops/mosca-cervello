from fastapi import FastAPI
import random
import time
import threading

app = FastAPI()

# cervello
neurons = [0.0] * 86
dopamine = 0.0

def give_dopamine(amount: float):
    global dopamine
    dopamine = 1.0
    for i in range(60, 86):
        neurons[i] = min(1.0, neurons[i] + amount)
    print(f"DOPAMINA +{amount}")

def decay_loop():
    global dopamine
    while True:
        time.sleep(0.5)
        dopamine = max(0.0, dopamine - 0.05)
        for i in range(86):
            neurons[i] = max(0.0, neurons[i] - 0.01)

threading.Thread(target=decay_loop, daemon=True).start()

@app.get("/")
def home():
    return {"status": "ONLINE", "dopamine": dopamine}

@app.post("/think")
def think(data: dict):
    dist = data.get("dist_to_door", 10)
    inc_dopa = data.get("dopamine", 0)

    mx = (random.random() - 0.5) * 2
    mz = (random.random() - 0.5) * 2

    if dist < 20:
        mx = -0.2
        mz = 0.5

    if dopamine > 0.1 or inc_dopa > 0.1:
        mx = mx * (1 + dopamine * 2)
        mz = mz * (1 + dopamine * 2)
        action = "gode"
    else:
        action = "cammina"

    spikes = sum(1 for n in neurons if n > 0.3)

    return {
        "move_x": mx,
        "move_z": mz,
        "spikes": spikes,
        "dopamine": dopamine,
        "action": action
    }

@app.post("/reward")
def reward(data: dict):
    amount = data.get("reward", 0.7)
    give_dopamine(amount)
    return {"ok": True, "dopamine": dopamine}
