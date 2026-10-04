from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.constants import CYCLE_LENGTH, POPULATION
from agents.population import create_population


st.set_page_config(page_title="Threshold | Agent Observatory", page_icon="T", layout="wide")

st.markdown(
    """
    <style>
    .block-container { max-width: 1400px; padding-top: 2rem; }
    h1, h2, h3 { letter-spacing: -0.04em; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("THRESHOLD")
st.title("Agent observatory")
st.write("Run the Python simulation and inspect how the population responds to pressure.")

with st.sidebar:
    st.header("Simulation controls")
    agent_count = st.number_input("Number of agents", min_value=1, max_value=200, value=POPULATION, step=1)
    cycle_length = st.number_input("Cycles per agent", min_value=1, max_value=1000, value=CYCLE_LENGTH, step=1)
    run_simulation = st.button("Run simulation", type="primary", use_container_width=True)
    st.caption("The simulation runs directly in Python. No web server or JSON import is required.")

if run_simulation:
    progress = st.progress(0, text="Starting simulation…")

    def update_progress(completed, total):
        progress.progress(completed / total, text=f"Running cycle {completed} of {total}…")

    with st.spinner("Running agents…"):
        st.session_state["result"] = create_population(
            int(agent_count),
            int(cycle_length),
            progress_callback=update_progress,
        )
    progress.empty()
    st.success("Simulation complete.")

result = st.session_state.get("result")
if result is None:
    st.info("Choose the population size and cycle count, then click **Run simulation**.")
    st.stop()

agents = result["agents"]
latest = pd.DataFrame([agent["history"][-1] for agent in agents])
history = pd.concat(
    [pd.DataFrame(agent["history"]).assign(agent=f"Agent {agent['id']}") for agent in agents],
    ignore_index=True,
)

metric_columns = st.columns(4)
metric_columns[0].metric("Population", result["simulation"]["population"])
metric_columns[1].metric("Cycles complete", result["simulation"]["cycles"])
metric_columns[2].metric("Average health", f"{latest['health'].mean():.1f} / 10")
metric_columns[3].metric("Average reward", f"{latest['reward'].mean():+.2f}")

st.subheader("Population response")
population_chart = history.groupby("cycle")[["health", "mood"]].mean()
st.line_chart(population_chart, height=300)

left, right = st.columns(2)
with left:
    st.subheader("Action mix")
    action_counts = history["action"].value_counts().reindex(
        ["Ignore", "Reduce Consumption", "Seek Support"], fill_value=0
    )
    st.bar_chart(action_counts)
with right:
    st.subheader("Average reward")
    st.line_chart(history.groupby("cycle")["reward"].mean(), height=260)

st.subheader("Agent snapshots")
snapshot = latest[["health", "mood", "action", "reward", "shock", "threshold", "epsilon"]].copy()
snapshot.insert(0, "Agent", [f"Agent {agent['id']}" for agent in agents])
st.dataframe(snapshot, use_container_width=True, hide_index=True)

selected_id = st.selectbox("Inspect agent", [agent["id"] for agent in agents], format_func=lambda value: f"Agent {value}")
selected = next(agent for agent in agents if agent["id"] == selected_id)
selected_history = pd.DataFrame(selected["history"]).set_index("cycle")

st.subheader(f"Agent {selected_id} detail")
detail_left, detail_right = st.columns([1, 1])
with detail_left:
    st.line_chart(selected_history[["health", "mood"]], height=260)
    st.dataframe(selected_history, use_container_width=True)
with detail_right:
    qtable = pd.DataFrame(
        selected["qtable"],
        columns=["Ignore", "Reduce Consumption", "Seek Support"],
    )
    qtable.index.name = "State"
    st.caption("Q-table · current values")
    st.dataframe(qtable.style.background_gradient(cmap="RdYlGn"), use_container_width=True)
