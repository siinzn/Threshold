from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm 
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

sns.set_theme()

class Params(NamedTuple):
    total_episodes: int
    learning_rate: float
    gamma: float
    epsilon: float
    map_size: int
    seed: int
    is_slippery: bool #noo idea
    n_runs: int
    action_size: int #possible actions 
    state_size: int # possible states
    proba_frozen: int


params = Params(
    total_episodes=2000,
    learning_rate=0.8,
    gamma=0.95,
    epsilon=0.1,
    map_size=5,
    seed=123,
    is_slippery=False,
    n_runs=20,
    action_size=None,
    state_size=None,
    proba_frozen=0.9
)

rng = np.random.default_rng(params.seed)

env = gym.make(
    "FrozenLake-v1",
    is_slippery=params.is_slippery,
    render_mode="rgb_array",
    desc=generate_random_map(
        size=params.map_size, p=params.proba_frozen, seed=params.seed
    ),
)   

params = params._replace(action_size=env.action_space.n)
params = params._replace(state_size=env.observation_space.n)

class Qlearning:
    def __init__(self, learning_rate, gamma, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.reset_qtable() 

    def update(self, state, action, reward, new_state):
        #bellman equation intution
        # new_Q = old_Q + learning_rate × (reward + gamma × max(next_state's Q-values) − old_Q)
        delta = (
        reward
        + self.gamma * np.max(self.qtable[new_state, :])
        - self.qtable[state, action]
        )
        q_update = self.qtable[state, action] + self.learning_rate * delta
        return q_update

    def reset_qtable(self):
        self.qtable = np.zeros((self.state_size, self.action_size))

class EpsilonGreedy:
    def __init__(self, epsilon):
        self.epsilon = epsilon
    
    def choose_action(self, action_space, state, qtable):
        explor_exploit_tradeoff = rng.uniform(0, 1)
        if explor_exploit_tradeoff < self.epsilon:
            action = action_space.sample()
        else:
            max_ids = np.where(qtable[state, :] == max(qtable[state, :]))[0]
            action = rng.choice(max_ids)
        
        return action
    

learner = Qlearning(
    params.learning_rate, params.gamma, params.state_size, params.action_size
)
explorer = EpsilonGreedy(params.epsilon)

def run():
    rewards = np.zeros((params.total_episodes, params.n_runs))
    steps = np.zeros((params.total_episodes, params.n_runs))
    episodes = np.arange(params.total_episodes)
    qtables = np.zeros((params.n_runs, params.state_size, params.action_size))
    all_states = []
    all_actions = []

    for run in range(params.n_runs):
        learner.reset_qtable()

        for episode in tqdm(episodes, desc=f"Run {run}/{params.n_runs} - Episdoes", leave=False):
            state = env.reset(seed=params.seed)[0]
            step = 0
            done = False
            total_rewards = 0

            while not done:
                action = explorer.choose_action(
                    action_space=env.action_space, state=state, qtable=learner.qtable
                )

                all_states.append(state)
                all_actions.append(action)

                new_state, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                learner.qtable[state, action] = learner.update(
                    state, action, reward, new_state
                )

                total_rewards += reward
                step += 1

                state = new_state
            rewards[episode, run] = total_rewards
            steps[episode, run] = step
        qtables[run, :, :] = learner.qtable

    return rewards, steps, episodes, qtables, all_states, all_actions

result = run()
rewards, steps, episodes, qtables, all_states, all_actions = result

print("Completed - Results")
print(f"{params.n_runs} runs × {params.total_episodes} episodes")
print(f"Avg last 100 episodes: {rewards[-100:].mean():.3f}")
print(f"Avg steps per episode: {steps.mean():.1f}")
print(f"Qtable shape: {qtables[-1].shape}")
print(f"State-Action pairs: {len(set(zip(all_states, all_actions)))}")
