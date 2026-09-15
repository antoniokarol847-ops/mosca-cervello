from fastapi import FastAPI
import random
import time
import threading

app = FastAPI()

# === CERVELLO 86 NEURONI + DOPAMINA VERA ===
neurons = [0.0]*86
dopamine = 0.0

def give_dopamine(amount: float):
    global dopamine
    dopamine = 1.0
    for i in range(60, 86):
        neurons[i] = min(1.0, neurons[i] + amount)
    print(f"🍖 DOPAMINA +{amount} -> neuroni 60-86 accesi! Livello: {dopamine}")

def decay_loop():
    global dopamine
    while True:
        dopamine = max(0.0, dopamine - 0.05)
        for i in range(86):
            neurons[i] = max(0.0, neurons[i] - 0.01)
        time.sleep(0.5)

# fa partire il calo della dopamina in background
threading.Thread(target=decay_loop, daemon=True).start()

@app.get("/")
def home():
    return {"status": "🧠 CERVELLO ONLINE", "neurons": 86, "dopamine": dopamine, "spikes": sum(1 for n in neurons if n > 0.5)}

@app.post("/think")
def think(data: dict):
    dist = data.get("dist_to_door", 10)
    incoming_dopa = data.get("dopamine", 0) # quella che arriva da Roblox

    mx = (random.random()-0.5)*2
    mz = (random.random()-0.5)*2

    # se è vicino alla porta, va dritto
    if dist < 20:
        mx = -0.2
        mz = 0.5

    # SE HA DOPAMINA, È FELICE E VA PIÙ VELOCE
    if dopamine > 0.1 or incoming_dopa > 0.1:
        mx *= (1 + dopamine * 2)
        mz *= (1 + dopamine * 2)

    spikes = sum(1 for n in neurons if n > 0.3)

    return {
        "move_x": mx,
        "move_z": mz,
        "spikes": spikes,
        "dopamine": dopamine,
        "action": "gode" if dopamine > 0.5 else "cammina"
    }

@app.post("/reward")
def reward(data: dict):
    amount = data.get("reward", 0.7)
    give_dopamine(amount)
    return {"ok": True, "dopamine": dopamine, "neurons_active": list(range(60, 86))}
