from fastapi import FastAPI
import random
import time
import threading

app = FastAPI()

neurons = [0.0] * 86
dopamine = 0.0

def give_dopamine(amount: float):
    global dopamine
    dopamine = 1.0
    for i in range(60, 86):
        if neurons[i] < 1.0:
            neurons[i] = min(1.0, neurons[i] + amount)
    print(f"DOPAMINA +{amount} -> {dopamine}")

def decay_loop():
    global dopamine
    while True:
        time.sleep(0.1)
        dopamine = max(0.0, dopamine - 0.02)
        for i in range(86):
            neurons[i] = max(0.0, neurons[i] - 0.05)

threading.Thread(target=decay_loop, daemon=True).start()

@app.get("/")
def home():
    return {"status": "ONLINE", "dopamine": dopamine}

@app.post("/think")
def think(data: dict):
    dist_door = data.get("dist_to_door", 10)
    dist_meat = data.get("dist_to_meat", 100)

    # NASO 40-60: odore carne
    if dist_meat < 30:
        for i in range(40, 60):
            neurons[i] = min(1.0, neurons[i] + 0.3)

    # GAMBE 0-30: pensano dove andare
    # le facciamo sparare sempre un po', così cammina
    for i in range(0, 30):
        if random.random() > 0.6:
            neurons[i] = random.uniform(0.2, 1.0)

    left_power = sum(neurons[0:10]) / 10.0
    right_power = sum(neurons[10:20]) / 10.0
    forward_power = sum(neurons[20:30]) / 10.0

    # movimento = cervello, non random
    move_x = (right_power - left_power) * 2.0
    move_z = (forward_power - 0.3) * 2.0

    # VISTA 30-40: vede porta
    if dist_door < 20:
        for i in range(30, 40):
            neurons[i] = 1.0
        move_z = move_z + 0.5

    if dopamine > 0.1:
        move_x = move_x * (1.0 + dopamine)
        move_z = move_z * (1.0 + dopamine)
        action = "gode"
    else:
        action = "cammina"

    spikes = sum(1 for n in neurons if n > 0.5)

    return {
        "move_x": move_x,
        "move_z": move_z,
        "spikes": spikes,
        "dopamine": dopamine,
        "neurons": neurons,
        "action": action
    }

@app.post("/reward")
def reward(data: dict):
    amount = float(data.get("reward", 0.7))
    give_dopamine(amount)
    return {"ok": True, "dopamine": dopamine}
