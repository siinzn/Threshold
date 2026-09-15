from .agent import Agent
import random
from agents.constants import choice_list, disease_list

def random_values():
    age_ = random.randint(18,55)
    gender_ = random.choice(["male", "female"]) 
    weight_ = random.randint(50,100)
    health_score_ = random.randint(1,10)
    savings_ = random.choice(list(choice_list.values())) 
    risk_tolerance_ = random.randint(1,10)
    social_support_ = random.choice(list(choice_list.values()))
    disease_ = random.choice(list(disease_list.values()))

    shock = []
    #shock_type = random.choice(list(shock_dict.values()))
    shock_intensity = random.random()
    #shock_duration = random.randint(1,10)
    shock.extend([shock_intensity])

    mood_ = random.randint(1,10)
    return age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_, shock, mood_

def run_agent_step(agent, shock):
    #shock will be added later

    print(f"Threshold : {agent.calculate_threshold()}")
    impact_ = agent.calculate_impact()

    print(f"Impact: {impact_}")
    action_= random.choice(agent.available_actions)

    reduced_impact_ = agent.apply_action(action=action_, impact=impact_)
    print(f"Reduced Impact : {reduced_impact_}")

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
    
    print(f"Reward: {round(reward_,2)}")
    return round(reward_,2)

def create_population(agent_count: int):
    population = []
    for i in range(agent_count):
        age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_,shock_,mood_ = random_values()
        agent_ = Agent(
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
        population.append(agent_)

    for ag in population:
        result = run_agent_step(agent=ag, shock=ag.shock)
        print(f"Results: {result}, Agent Health: {ag.health}\n")

create_population(4)