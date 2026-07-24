from .agent import Agent
import random
import pprint

"""
i want to create 10 agents with a set of ranged values
1 - create a function that gets random values
2 - run a loop
but how do i run a set of a agents. i want to set a range for 10 agents so that i can have a range of agent traits rather than being fully random
"""

def random_values():
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
    age_ = random.randint(18,55)
    gender_ = random.choice(["male", "female"]) 
    weight_ = random.randint(50,100)
    health_score_ = random.randint(1,10)
    savings_ = random.choice(list(choice_list.values())) 
    risk_tolerance_ = random.randint(0,10)
    social_support_ = random.choice(list(choice_list.values()))
    disease_ = random.choice(list(disease_list.values()))
    return age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_


def create_population(agent_count: int):
    population = []  
    for i in range(agent_count):
        age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_ = random_values()
        agent = Agent(age=age_, gender=gender_, weight=weight_, health=health_score_,savings=savings_,risk_tolerance=risk_tolerance_,social_support=social_support_,disease=disease_)
        population.append(agent)
        print(f"Agent : {i} Added to population")
        pprint.pprint(vars(population[i]), sort_dicts=False)
        print(f"\nThreshold : {agent.calculate_threshold()}")
        print("\n")
    return population

create_population(10)    