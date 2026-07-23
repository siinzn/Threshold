import random
import pprint

class Agent:
    def __init__(self, 
                age: int, 
                gender: str,
                weight: int, 
                health: int,
                savings: str,
                risk_tolerance: int,
                social_support: str,
                disease: str,
                 ):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.health = health
        self.savings = savings
        self.risk_tolerance = risk_tolerance
        self.social_support = social_support
        self.disease = disease

"""
i want to create 10 agents with a set of ranged values
1 - create a function that gets random values
2 - run a loop
but how do i run a set of a agents. i want to set a range for 10 agents so that i can have a range of agent traits rather than being fully random

"""