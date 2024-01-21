import time
import os
import random

# starts running once reroll is pressed

die_art = {
    0: ["┌─────────┐",
        "│         │",
        "│         │",
        "│         │",
        "└─────────┘"
        ],
    1: ["┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"
        ],
    2: ["┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"
        ],
    3: ["┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"
        ],
    4: ["┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"
        ],
    5: ["┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"
        ],
    6: ["┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"
        ]
}

def show_dice(dices):
    for i in range(5):
        print(' '.join(die_art[n][i] for n in dices))

def roll_dice(dice, fixed_index):
    timeout = time.time() + 2   # 7 seconds
    
    while time.time() < timeout:
        dtp = [random.randint(1, 6) if not fixed_index[i] else dice[i] for i in range(5)]
        show_dice(dtp)
        
        os.system('clear')
        time.sleep(0.003)