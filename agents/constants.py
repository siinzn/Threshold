choice_list = {
    "None": 0.0,
    "Some": 0.5,
    "Large": 1.0
}
disease_list = {
    #0 means it doesnt affect the agent, number closer to the 1.0 affects way more
        "None": 0.0,
        "Diabetes": 0.3,
        "Hypertension": 0.3,
        "Asthma": 0.3
    }
shock_dict = {
    "Supply Decrease": 6,
    "Global Pandamic": 8,
    "Job Loss": 9,
    "War": 10
}

action_cost = {
    "Ignore" : 0,
    "Reduce Consumption" : 0.05,
    "Seek Support" : 0.1
}