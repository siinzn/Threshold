
class SimulationRecorder:
    def __init__(self, agent_count, cycle_length, progress_callback=None):
        # These values tell the recorder how much work the simulation has to do.
        self.agent_count = agent_count
        self.cycle_length = cycle_length
        # Streamlit gives us this function so it can update its progress bar.
        self.progress_callback = progress_callback
        # Each agent gets its own list of cycle results.
        self.history_by_agent = {}

    def add_agent(self, agent):
        # Start with an empty history before the agent begins its cycles.
        self.history_by_agent[agent.id] = []

    def record_cycle(
        self,
        agent,
        cycle_number,
        shock,
        threshold,
        impact,
        action,
        reward,
    ):
        # Save a simple snapshot of the agent after this cycle.
        # This is only for observing the simulation; it does not change the agent.
        self.history_by_agent[agent.id].append({
            "cycle": cycle_number,
            "shock": round(shock, 4),
            "threshold": round(threshold, 2),
            "impact": round(impact, 2),
            "action": action,
            "reward": reward,
            "health": round(agent.health, 2),
            "mood": round(agent.mood, 2),
            "epsilon": round(agent.epsilon, 4),
        })

        if self.progress_callback is not None:
            # Work out how far through the whole population we are.
            # For example, after agent 2 cycle 3, several cycles have already finished.
            completed_steps = (
                (agent.id - 1) * self.cycle_length
                + cycle_number
            )
            total_steps = self.agent_count * self.cycle_length

            # Tell Streamlit to move its progress bar forward.
            self.progress_callback(
                completed_steps,
                total_steps,
            )

    def build_result(self, population):
        # Turn the recorded histories and final Q-tables into one result
        # that Streamlit can use for charts, tables, and agent details.
        agents = []

        for agent in population:
            # Combine the agent's traits, history, and learned Q-table.
            agents.append({
                "id": agent.id,
                "age": agent.age,
                "gender": agent.gender,
                "riskTolerance": agent.risk_tolerance,
                "socialSupport": agent.social_support,
                "history": self.history_by_agent[agent.id],
                "qtable": agent.qtable.tolist(),
            })

        return {
            # This gives the dashboard a quick summary of the run.
            "simulation": {
                "cycles": self.cycle_length,
                "population": len(population),
            },
            "agents": agents,
        }