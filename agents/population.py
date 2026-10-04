from .agent import Agent
import random
import numpy as np
from simulation.simulation import SimulationRecorder
from agents.constants import (
    CHOISE_DICT, 
    DISEASE_DICT, 
    AVAILABLE_ACTIONS, 
    CYCLE_LENGTH, 
    POPULATION, 
    LEARNING_RATE, 
    GAMMA, 
    EPSILON_DECAY, 
    EPSILON_MIN
)

def random_values():
    # Most of them are random for now so every run creates a different population.
    age_ = random.randint(18,55)
    gender_ = random.choice(["male", "female"]) 
    weight_ = random.randint(50,100)
    health_score_ = random.randint(1,10)
    savings_ = random.choice(list(CHOISE_DICT.values())) 
    risk_tolerance_ = random.randint(1,10)
    social_support_ = random.choice(list(CHOISE_DICT.values()))
    disease_ = random.choice(list(DISEASE_DICT.values()))

    # The first shock is saved on the agent, and new shocks are made during the cycles below.
    shock = []
    shock_intensity = random.random()
    shock.extend([shock_intensity])

    mood_ = random.randint(1,10)
    return age_,gender_,weight_,health_score_,savings_,risk_tolerance_,social_support_,disease_, shock, mood_

def get_state(agent):
    # Health and mood are floats, but the Q-table needs a small whole-number state, Dividing them into buckets gives us 25 possible health/mood combinations.
    b_health = min(agent.health // 2, 4)
    b_mood = min(agent.mood // 2, 4)    
    return int(b_health * 5 + b_mood)

def run_agent_step(agent, shock):
    # This is one complete shock -> action -> reward -> learning cycle for one agent.
    agent.shock = shock
    impact_ = agent.calculate_impact()

    # The agent looks at its current health and mood bucket before choosing.
    state_id = get_state(agent=agent)
    random_float = random.random()

    # Early on, epsilon is high, so the agent usually explores random actions.
    # Later, it starts using the action with the best value in its Q-table.
    if random_float < agent.epsilon:
        action_= random.choice(AVAILABLE_ACTIONS)
    else:
        max_idx = np.where(agent.qtable[state_id] == max(agent.qtable[state_id]))[0]
        action_ = AVAILABLE_ACTIONS[random.choice(max_idx)]

    # The chosen action can make the impact smaller before health and mood are updated.
    reduced_impact_ = agent.apply_action(action=action_, impact=impact_)

    # Save the old values because the reward is based on what changed.
    old_health_ = agent.health
    old_mood_ = agent.mood

    agent.update_state(reduced_impact=reduced_impact_, action=action_)

    # This is the state after the action. Q-learning compares the old and new states.
    next_state_id = get_state(agent=agent)
    action_index = AVAILABLE_ACTIONS.index(action_)

    # Reward tells the agent whether the action helped or hurt overall.
    reward_ = agent.agent_reward(
        old_health=old_health_, 
        health=agent.health,
        old_mood=old_mood_,
        mood=agent.mood,
        action=action_
        )

    agent.update_qtable(state_id,action_index,reward_, next_state_id, GAMMA, LEARNING_RATE)
    agent.epsilon = max(agent.epsilon * EPSILON_DECAY, EPSILON_MIN)
    return round(reward_,2), action_

"""
so what i want is, one agent needs to go through n times of shock and reward cycle. So i need to have a loop which runs for the number of agent count and then an inner loop that runs n number of times
so we put a single agent through multiple cycles. it seems pretty straight forward
"""

def create_population(
    agent_count: int,
    cycle_length: int = CYCLE_LENGTH,
    progress_callback=None,
):
    population = []

    # Streamlit uses this data later to draw charts and tables.
    recorder = SimulationRecorder(
        agent_count=agent_count,
        cycle_length=cycle_length,
        progress_callback=progress_callback,
    )

    # Create each agent, then put that same agent through all of its cycles.
    for i in range(agent_count):
        (
            age_,
            gender_,
            weight_,
            health_score_,
            savings_,
            risk_tolerance_,
            social_support_,
            disease_,
            shock_,
            mood_,
        ) = random_values()

        # These random traits become the starting point for this agent.
        agent = Agent(
            id=i + 1,
            age=age_,
            gender=gender_,
            weight=weight_,
            health=health_score_,
            savings=savings_,
            risk_tolerance=risk_tolerance_,
            social_support=social_support_,
            disease=disease_,
            shock=shock_,
            mood=mood_,
        )

        population.append(agent)
        recorder.add_agent(agent)

        # Every cycle gives the agent a new shock and lets it learn from its response.
        for cycle_number in range(1, cycle_length + 1):
            shock_intensity = random.random()
            shock = [shock_intensity]

            reward, action = run_agent_step(
                agent=agent,
                shock=shock,
            )

            # Save the important values from this cycle for the dashboard.
            recorder.record_cycle(
                agent=agent,
                cycle_number=cycle_number,
                shock=shock_intensity,
                threshold=agent.calculate_threshold(),
                impact=agent.calculate_impact(),
                action=action,
                reward=reward,
            )

    return recorder.build_result(population)


if __name__ == "__main__":
    create_population(POPULATION)