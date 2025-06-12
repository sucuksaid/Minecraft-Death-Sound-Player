
from playsound import playsound
import random
import time
import os

# === CONFIGURATION ===
log_path = r"C:\Path\To\Your\Minecraft\Logs\latest.log" #path to minecraft latest log file
player_name = "player name" #your player name

sounds = [  #dont forget to add sound names
    "testrec1.mp3", "testrec2.mp3", "testrec3.mp3", "testrec4.mp3",
    "testrec5.mp3", "testrec6.mp3", "testrec7.mp3", "testrec8.mp3"
] 

death_keywords = [   #TODO: write all of death keywords correctly
    "fell",
    "slain",
    "died",
    "blew up",
    "elytra",
    "burned",
    "exploded",
    "was shot",
    "hit the ground too hard",
    "lava",
    "fire",
    "void",
    "starved",
    "walked into a cactus",
    "killed",
]

# === LOG FOLLOW FUNCTION ===
def follow_log(path):
    with open(path, "r", encoding="utf-8") as f:
        f.seek(0, 2)  # Move to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                try:
                    if os.path.getsize(path) < f.tell():
                        return  # Log rotated or truncated
                except FileNotFoundError:
                    return
                continue
            yield line

# === MAIN LOOP ===
cooldown = 0  #its not necessary but I'm afraid it might break let's just leave it
last_detection_time = 0 #same

while True:
    for line in follow_log(log_path):
        low = line.lower()

        # Only allow lines from server thread
        if "[server thread" not in low:
            continue

        # Ignore chat-like lines: [Not Secure] <Player> message
        if "<" in line and ">" in line:
            continue

        # Detect if player's name and a death keyword are both in line
        if player_name.lower() in low:
            if any(keyword in low for keyword in death_keywords):
                current_time = time.time()
                if current_time - last_detection_time < cooldown:
                    continue  # Skip if in cooldown
                print("Minecraft death detected:", line.strip())
                playsound(random.choice(sounds))
                last_detection_time = current_time

    time.sleep(1) #checking for deaths delay
