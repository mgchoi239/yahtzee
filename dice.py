import time
import os
import random

# starts running once reroll is pressed

die_art = {
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

timeout = time.time() + 2   # 7 seconds

sample = [-1, 2, 3, -1, -1]

while time.time() < timeout:
    dtp = [random.randint(1, 6) if sample[i] == -1 else sample[i] for i in range(5)]

    for i in range(5):
        print(' '.join(die_art[n][i] for n in dtp))
        
    os.system('clear')
    time.sleep(0.003)