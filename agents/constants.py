CHOISE_DICT = {
    "None": 0.0,
    "Some": 0.5,
    "Large": 1.0
}
DISEASE_DICT = {
    #0 means it doesnt affect the agent, number closer to the 1.0 affects way more
        "None": 0.0,
        "Diabetes": 0.3,
        "Hypertension": 0.3,
        "Asthma": 0.3
    }
SHOCK_DICT = {
    "Supply Decrease": 6,
    "Global Pandamic": 8,
    "Job Loss": 9,
    "War": 10
}

AVAILABLE_ACTIONS = [
    "Ignore",
    "Reduce Consumption",
    "Seek Support",
]

ACTION_COST = {
    "Ignore" : 0,
    "Reduce Consumption" : 0.05,
    "Seek Support" : 0.1
}

POPULATION = 5
CYCLE_LENGTH = 100

LEARNING_RATE = 0.1
GAMMA = 0.95