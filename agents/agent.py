from agents.constants import ACTION_COST
import numpy as np

class Agent:
    def __init__(self, 
                id: int,
                age: int, 
                gender: str,
                weight: int, 
                health: int,
                savings: float,
                risk_tolerance: int,
                social_support: float,
                disease: float,
                shock: list,
                mood: int
                 ):
        self.id = id
        self.age = age
        self.gender = gender
        self.weight = weight
        self.health = health
        self.savings = savings
        self.risk_tolerance = risk_tolerance
        self.social_support = social_support
        self.disease = disease
        self.shock = shock
        self.mood = mood
        self.state_size = 25
        self.action_size = 3
        self.epsilon = 1.0
        self.qtable = np.zeros((self.state_size, self.action_size))

    def calculate_threshold(self):
        threshold = ((self.health/10) + (self.risk_tolerance/10) + self.savings + self.social_support - self.disease)/4 #disease is penalizing hence dividing by 4 to normalize
        return round(threshold, 2)

    def calculate_impact(self):
        threshold_ = self.calculate_threshold()
        shock_ = self.shock[0]
        #print(round(shock_,2))
        impact = 0
        if  round(shock_,2) <= threshold_:
            #print("safe")
            return impact
        else:
            impact = shock_ - threshold_
            #print("unsafe")
            return round(impact,2)

    """
    this is my idea here, if an agent has a low impact value which means the impact wasnt bad, then he can jsut ignore it. lets say imapct was due to his salary/savings being low then he should 
    reduce consumption. if the impact - actually im hella lost on this. i think the issue is that im not adding everything as in all traits and what not so im having to cut things off and cant think 
    straight. 
    """
    def apply_action(self, action, impact):
        if action == "Ignore":
            #print(f"Agent action : Ignore impact")
            return impact #my idea was if impact is small ignore it

        #this actually depends on salary so for now ill just keep it for savings
        elif action == "Reduce Consumption":
            #print(f"Agent action : Reduce Consumption")
            #im just gonna randomly guess a number to reduce from the impact since we havent set a metric for it
            if impact != 0:
                impact -= 0.05
            return round(impact,2)

        #if an agent has good social support then he can get help from them to reduce impact
        elif action == "Seek Support":
            #print(f"Agent action : Seek Support")
            if impact != 0:
                if self.social_support >= 0.7:
                    #print(f"insane support: {self.social_support}")
                    impact -= 0.07
                else:
                    impact -= 0.02 #i just decided a random number so yeah
            return round(impact,2)

    def update_state(self, reduced_impact):
        self.health -= reduced_impact * 10
        self.health = max(0, min(10, self.health))

        self.mood -= reduced_impact * 10
        self.mood = max(0, min(10, self.mood))

        # this is after the agent gets hit by a shock and how it recovers
        # i dont need to have and if statement to keep the health and mood under 10 because max and min already handles that
        if self.risk_tolerance <= 5:
            self.health += 0.4
            self.mood += 0.4
        else:
            self.health += 1
            self.mood += 1

    def agent_reward(self, old_health, health, old_mood, mood, action):
        action_cost_ = ACTION_COST[action]
        reward = (health - old_health) + (mood - old_mood) - action_cost_
        return reward

    def update_qtable(self, state_id, action_index, reward,next_state_id, gamma, learning_rate):
        delta = reward + gamma * max(self.qtable[next_state_id]) - self.qtable[state_id, action_index]
        self.qtable[state_id, action_index] += learning_rate * delta
         