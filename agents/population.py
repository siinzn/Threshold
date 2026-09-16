from .agent import Agent
import random
from agents.constants import CHOISE_DICT, DISEASE_DICT, AVAILABLE_ACTIONS, CYCLE_LENGTH, POPULATION

def random_values():
    age_ = random.randint(18,55)
    gender_ = random.choice(["male", "female"]) 
    weight_ = random.randint(50,100)
    health_score_ = random.randint(1,10)
    savings_ = random.choice(list(CHOISE_DICT.values())) 
    risk_tolerance_ = random.randint(1,10)
    social_support_ = random.choice(list(CHOISE_DICT.values()))
    disease_ = random.choice(list(DISEASE_DICT.values()))

    shock = []
    #shock_type = random.choice(list(shock_dict.values()))
    shock_intensity = random.random()
    #shock_duration = random.randint(1,10)
    shock.extend([shock_intensity])

    mood_ = random.randint(1,10)
    return age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_, shock, mood_

def run_agent_step(agent, shock):
    agent.shock = shock

    #print(f"Threshold : {agent.calculate_threshold()}")
    impact_ = agent.calculate_impact()

    #print(f"Impact: {impact_}")
    action_= random.choice(AVAILABLE_ACTIONS)

    reduced_impact_ = agent.apply_action(action=action_, impact=impact_)
    #print(f"Reduced Impact : {reduced_impact_}")

    old_health_ = agent.health
    old_mood_ = agent.mood

    agent.update_state(reduced_impact=reduced_impact_)

    reward_ = agent.agent_reward(
        old_health=old_health_, 
        health=agent.health,
        old_mood=old_mood_,
        mood=agent.mood,
        action=action_
        )
    
    #print(f"Reward: {round(reward_,2)}")
    return round(reward_,2), action_

"""
so what i want is, one agent needs to go through n times of shock and reward cycle. So i need to have a loop which runs for the number of agent count and then an inner loop that runs n number of times
so we put a single agent through multiple cycles. it seems pretty straight forward
"""

def create_population(agent_count: int):
    population = []
    for i in range(agent_count):
        age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_,shock_,mood_ = random_values()
        agent_ = Agent(
            id=i,
            age=age_, 
            gender=gender_, 
            weight=weight_, 
            health=health_score_,
            savings=savings_,
            risk_tolerance=risk_tolerance_,
            social_support=social_support_,
            disease=disease_, 
            shock=shock_, 
            mood=mood_
            )
        #print(f"Agent ID: {agent_.id}")
        population.append(agent_)
        #inner loop to put an agent through n number of cycles
        for j in range(CYCLE_LENGTH):
            new_shock=[]
            new_shock_intensity = random.random()
            new_shock.extend([new_shock_intensity])
            reward_, action_ = run_agent_step(agent=agent_, shock=new_shock)
            print(f"[Agent {agent_.id}] | Cycle {j} | Action: {action_} | Reward: {reward_} | Health: {round(agent_.health,2)} | Mood: {round(agent_.mood,2)}\n")

    """
    for ag in population:
        result = run_agent_step(agent=ag, shock=ag.shock)
        print(f"Results: {result}, Agent Health: {ag.health}\n")
    """
create_population(POPULATION)