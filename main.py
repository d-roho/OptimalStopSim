import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from optimal_stopping import simulate_optimal_stopping
from utils import generate_sample_sequence, calculate_statistics

# Page configuration
st.set_page_config(page_title="Russell's Optimal Stopping Problem Simulator",
                   layout="wide")

# Title and introduction
st.title("📊 Russell's Optimal Stopping Problem Simulator")

st.markdown("""
This simulator demonstrates the Optimal Stopping Problem, also known as the "Secretary Problem" 
or the "37% Rule". The problem involves deciding when to stop searching and make a selection 
to maximize the probability of choosing the best option.

### Problem Rules:
1. You see a sequence of options one at a time
2. For each option, you must decide to select it or continue searching
3. You can't go back to previous options
4. The goal is to select the best option
""")

# Additional explanation
st.markdown("""
### Optimal Strategy

The optimal stopping strategy now follows these rules:
1. Observe the first portion of options without making a selection (looking phase)
2. After the looking phase, select the first option that is at least as good as the specified percentage of the best value seen so far
3. If no suitable option is found, select the last option

### Alternative Scenarios

The "Stopping Threshold %" parameters allows you to be more flexible in your selection criteria:
- 100%: Only select options that are at least as good as the best seen value
- Lower values: Accept options that are close enough to the best seen value

The "Looking Phase Ratio" determines the proportion of items to observe before making a decision. Traditionally, this is set based on the Stopping Threshold. In reality, this should be set as the % of your search you that believe has been completed thus far.

### **Empirical Values for Alternative Scenarios**
| Stopping Threshold %) | Optimal Looking Ratio | Success Rate (Selecting Best) | Failure Rate (Selecting None)
|--------------------|--------------------------------------|-------------------------------|-------------------------------|
| 100% (Classic)     | ~37%                                 | ~37%                          | ~37% |
| 90%                | ~30%                                 | ~25%                          | ~10% |
| 80%                | ~25%                                 | ~15%                          | ~1% |
| 70%                | ~20%                                 | ~10%                          | ~0% |

AFAIK, the above empirical values (except Failure Rate, where N = 100) asssume N tends to infinity, and were calculated using Deepseek R1. I calculated the Failure Rate using this simulator.
""")

# User input
# Sidebar controls
st.sidebar.header("Simulation Parameters")

n_items = st.sidebar.slider("Number of Items",
                           min_value=5,
                           max_value=200,
                           value=100,
                           help="Total number of items to choose from")

n_simulations = st.sidebar.slider("Number of Simulations",
                                 min_value=1000,
                                 max_value=1000000,
                                 value=100000,
                                 step=1000,
                                 help="Number of times to run the simulation")

threshold_ratio = st.sidebar.slider(
    "Stopping Threshold %",
    min_value=0,
    max_value=100,
    value=100,
    help=
    "Accept values that are at least this percentage as good as the best seen value"
) / 100.0

look_ratio = st.sidebar.slider(
    "Looking Phase Ratio",
    min_value=0.0,
    max_value=1.0,
    value=0.37,
    step=0.01,
    help=
    "Proportion of items to observe before making a decision. Default is 37%, traditionally set proportionate to Stopping Threshold."
)

# Run simulation
if st.button("Run Simulation"):
    start_time = datetime.now()

    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.spinner(f'Running {n_simulations:,} simulations...'):
        # Update status
        status_text.text(f"Starting simulation with {n_simulations:,} iterations...")

        results = simulate_optimal_stopping(n_items, n_simulations, look_ratio,
                                         threshold_ratio)
        stats = calculate_statistics(results)

        # Clear progress indicators
        progress_bar.progress(100)
        status_text.empty()

        # Show completion message
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        st.success(f"""
        ✅ Simulation completed successfully!
        - Time taken: {duration:.2f} seconds
        - Iterations: {n_simulations:,}
        - Items per sequence: {n_items}
        """)

        # Display results
        st.subheader("Simulation Results")

        # Statistics tabs
        tab1, tab2 = st.tabs(["Mean Statistics", "Median Statistics"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Best Option Pick Rate", f"{stats['success_rate']:.2%}")
                st.metric("Average Stopping Position",
                         f"{stats['avg_position']:.0f}th item")
            with col2:
                st.metric("Failure Rate (None match threshold)",
                         f"{stats['failure_rate']:.2%}")
                st.metric("Average Selected Value as % of Best Value",
                         f"{stats['best_value_rate']:.2%}")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Median Stopping Position",
                         f"{stats['median_position']:.0f}th item")
                st.metric("Median Selected Value",
                         f"{stats['median_value']:.2f}")
            with col2:
                st.metric("Median Best Possible Value",
                         f"{stats['median_best_possible']:.2f}")
                st.metric("Median Selected Value as % of Best Value",
                         f"{stats['median_value_rate']:.2f}")

        # Example sequence visualization
        sample_sequence = generate_sample_sequence(n_items)
        look_phase = int(n_items * look_ratio)

        fig = go.Figure()

        # Add looking phase
        fig.add_trace(
            go.Scatter(x=list(range(look_phase)),
                       y=sample_sequence[:look_phase],
                       mode='lines+markers',
                       name='Looking Phase',
                       line=dict(color='gray')))

        # Highlight max value in looking phase
        look_max_index = np.argmax(sample_sequence[:look_phase])
        fig.add_trace(
            go.Scatter(x=[look_max_index],
                       y=[sample_sequence[look_max_index]],
                       mode='markers',
                       marker=dict(size=10, color='blue'),
                       name='Looking Phase Max'))

        # Add selection phase
        fig.add_trace(
            go.Scatter(x=list(range(look_phase, n_items)),
                       y=sample_sequence[look_phase:],
                       mode='lines+markers',
                       name='Selection Phase',
                       line=dict(color='purple')))

        # Find the first value in the selection phase that meets the threshold
        selected_value_index = -1
        for i in range(look_phase, n_items):
            current_value = sample_sequence[i]
            if current_value >= threshold_ratio * sample_sequence[look_max_index]:
                selected_value_index = i
                break

        # Highlight the first value meeting the threshold
        if selected_value_index != -1:
            fig.add_trace(
                go.Scatter(x=[selected_value_index],
                           y=[sample_sequence[selected_value_index]],
                           mode='markers',
                           marker=dict(size=10, color='green'),
                           name='Selected Value'))

        # Highlight the last value if none meet threshold
        if selected_value_index == -1:
            fig.add_trace(
                go.Scatter(x=[n_items - 1],
                           y=[sample_sequence[n_items - 1]],
                           mode='markers',
                           marker=dict(size=10, color='red'),
                           name='Selected Value (None met threshold)'))

        # Highlight max value in selection phase
        sel_max_index = np.argmax(sample_sequence[look_phase:])
        fig.add_trace(
            go.Scatter(x=[look_phase + sel_max_index],
                       y=[sample_sequence[look_phase + sel_max_index]],
                       mode='markers',
                       marker=dict(size=12, color='Yellow'),
                       name='Hindsight Max'))

        # Highlight if selected is best
        if selected_value_index == look_phase + sel_max_index:
            fig.add_trace(
                go.Scatter(x=[look_phase + sel_max_index],
                           y=[sample_sequence[look_phase + sel_max_index]],
                           mode='markers',
                           marker=dict(size=20, symbol='diamond', color='Yellow'),
                           name='Selected Value == Hindsight Max'))

        # Add title and axis labels
        fig.update_layout(title="Example Sequence",
                          xaxis_title="Position",
                          yaxis_title="Value",
                          showlegend=True)

        st.plotly_chart(fig, use_container_width=True)

        # Distribution plots
        # Value comparison histogram
        fig_values = go.Figure()

        # Add selected values histogram
        fig_values.add_trace(
            go.Histogram(x=results['value'],
                         name='Selected Values',
                         nbinsx=30,
                         marker_color='blue',
                         opacity=0.6))

        # Add maximum possible values histogram
        fig_values.add_trace(
            go.Histogram(x=results['best_possible'],
                         name='Maximum Values',
                         nbinsx=30,
                         marker_color='red',
                         opacity=0.6))

        # Add median lines
        fig_values.add_vline(x=stats['median_value'],
                            line_dash="dash",
                            line_color="blue",
                            annotation_text="Median Selected Value")
        fig_values.add_vline(x=stats['median_best_possible'],
                            line_dash="dash",
                            line_color="red",
                            annotation_text="Median Best Possible")

        fig_values.update_layout(
            title="Distribution of Selected vs Maximum Values",
            xaxis_title="Value",
            yaxis_title="Frequency",
            barmode='overlay')
        st.plotly_chart(fig_values, use_container_width=True)

        # Distribution of selected positions
        fig_dist = px.histogram(results,
                               x="position",
                               title="Distribution of Selected Positions",
                               labels={
                                   "position": "Position",
                                   "count": "Frequency"
                               },
                               nbins=n_items)

        # Add median line
        fig_dist.add_vline(x=stats['median_position'],
                          line_dash="dash",
                          line_color="red",
                          annotation_text="Median Position")

        fig_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)