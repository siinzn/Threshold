
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
                shock: list,
                available_actions: str
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
        self.available_actions = available_actions

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
        impact = self.calculate_impact()
        if action == "Ignore":
            print(f"Agent action : Ignore impact")
            return impact #my idea was if impact is small ignore it

        #this actually depends on salary so for now ill just keep it for savings
        elif action == "Reduce Consumption":
            print(f"Agent action : Reduce Consumption")
            #im just gonna randomly guess a number to reduce from the impact since we havent set a metric for it
            if impact != 0:
                impact -= 0.05
            return round(impact,2)

        #if an agent has good social support then he can get help from them to reduce impact
        elif action == "Seek Support":
            print(f"Agent action : Seek Support")
            if impact != 0:
                impact -= 0.07 #i just decided a random number so yeah
            return round(impact,2)