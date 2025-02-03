import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from optimal_stopping import simulate_optimal_stopping
from utils import generate_sample_sequence, calculate_statistics

# Page configuration
st.set_page_config(
    page_title="Optimal Stopping Problem Simulator",
    layout="wide"
)

# Title and introduction
st.title("📊 Optimal Stopping Problem Simulator")

st.markdown("""
This simulator demonstrates the Optimal Stopping Problem, also known as the "Secretary Problem" 
or the "37% Rule". The problem involves deciding when to stop searching and make a selection 
to maximize the probability of choosing the best option.

### How it works:
1. You see a sequence of options one at a time
2. For each option, you must decide to select it or continue searching
3. You can't go back to previous options
4. The goal is to select the best option
""")

# Sidebar controls
st.sidebar.header("Simulation Parameters")

n_items = st.sidebar.slider(
    "Number of Items",
    min_value=5,
    max_value=100,
    value=20,
    help="Total number of items to choose from"
)

n_simulations = st.sidebar.slider(
    "Number of Simulations",
    min_value=100,
    max_value=10000,
    value=1000,
    help="Number of times to run the simulation"
)

look_ratio = st.sidebar.slider(
    "Looking Phase Ratio",
    min_value=0.0,
    max_value=1.0,
    value=0.37,
    step=0.01,
    help="Proportion of items to observe before making a decision (0.37 is optimal for large N)"
)

# Run simulation
if st.button("Run Simulation"):
    results = simulate_optimal_stopping(n_items, n_simulations, look_ratio)
    stats = calculate_statistics(results)
    
    # Display results in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Simulation Results")
        st.metric("Success Rate", f"{stats['success_rate']:.2%}")
        st.metric("Average Position Selected", f"{stats['avg_position']:.2f}")
        st.metric("Best Possible Value Rate", f"{stats['best_value_rate']:.2%}")
    
    # Example sequence visualization
    with col2:
        sample_sequence = generate_sample_sequence(n_items)
        look_phase = int(n_items * look_ratio)
        
        fig = go.Figure()
        
        # Add looking phase
        fig.add_trace(go.Scatter(
            x=list(range(look_phase)),
            y=sample_sequence[:look_phase],
            mode='lines+markers',
            name='Looking Phase',
            line=dict(color='gray')
        ))
        
        # Add selection phase
        fig.add_trace(go.Scatter(
            x=list(range(look_phase, n_items)),
            y=sample_sequence[look_phase:],
            mode='lines+markers',
            name='Selection Phase',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title="Example Sequence",
            xaxis_title="Position",
            yaxis_title="Value",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution of selected positions
    fig_dist = px.histogram(
        results,
        x="position",
        title="Distribution of Selected Positions",
        labels={"position": "Position", "count": "Frequency"},
        nbins=n_items
    )
    fig_dist.update_layout(showlegend=False)
    st.plotly_chart(fig_dist, use_container_width=True)

# Additional explanation
st.markdown("""
### Strategy Details

The optimal strategy for the stopping problem follows these rules:
1. Observe the first 37% of options without making a selection (looking phase)
2. After the looking phase, select the first option that is better than all previously seen options
3. If no better option is found, select the last option

This 37% rule is mathematically proven to be optimal as the number of options approaches infinity.
""")
