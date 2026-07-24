import math

class Agent:
    def __init__(self, 
                age: int, 
                gender: str,
                weight: int, 
                health: int,
                savings: float,
                risk_tolerance: int,
                social_support: float,
                disease: float,
                shock: list
                 ):
        self.age = age
        self.gender = gender
        self.weight = weight
        self.health = health
        self.savings = savings
        self.risk_tolerance = risk_tolerance
        self.social_support = social_support
        self.disease = disease
        self.shock = shock

    def calculate_threshold(self):
        threshold = ((self.health/10) + (self.risk_tolerance/10) + self.savings + self.social_support - self.disease)/4 #disease is penalizing hence dividing by 4 to normalize
        return round(threshold, 2)

    def calculate_impact(self):
        threshold_ = self.calculate_threshold()
        shock_ = (self.shock[0] + self.shock[1] + self.shock[2] ) / 3
        if  round(shock_,2) > threshold_:
            print(f"Impact: not safe")
            return round(shock_,2)
        else:
            print(f"Impact: safe")
            return round(shock_,2)