from .agent import Agent
import random
import pprint

def create_random_agents():
    age_ = random.randint(18,55)
    gender_ = random.choice(["male", "female"]) 
    weight_ = random.randint(50,100)
    health_score_ = random.randint(1,10)
    savings_ = random.choice(["None", "Some", "Large"]) 
    risk_tolerance_ = random.randint(0,10)
    social_support_ = random.choice(["None", "Some", "Large"])
    disease_ = random.choice(["None","Diabetes","Hypertension","Asthma"])
    return age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_


def create_population(agent_count: int):
    population = []  
    for i in range(agent_count):
        age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_ = create_random_agents()
        agent = Agent(age=age_, gender=gender_, weight=weight_, health=health_score_,savings=savings_,risk_tolerance=risk_tolerance_,social_support=social_support_,disease=disease_)
        population.append(agent)
        print(f"Agent : {i} Added to population")
        pprint.pprint(vars(population[i]), sort_dicts=False)
        print("\n")
    return population

create_population(10)