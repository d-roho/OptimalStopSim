
# Russell's Optimal Stopping Problem Simulator

This Streamlit application simulates the Optimal Stopping Problem, also known as the "Secretary Problem" or the "37% Rule". It demonstrates how to optimize decision-making when selecting from a sequence of options.

## Features

- Interactive simulation parameters
- Real-time visualization of results
- Statistical analysis of outcomes
- Example sequence visualization
- Distribution plots of selected vs maximum values

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Running the Application

The application runs using Streamlit. Clone this repo to your environment. To start:

```bash
streamlit run main.py
```

## Parameters

- **Number of Items**: Total number of items to choose from (5-200)
- **Number of Simulations**: Number of times to run the simulation (1,000-1,000,000)
- **Stopping Threshold %**: Minimum acceptable value relative to the best seen
- **Looking Phase Ratio**: Proportion of items to observe before making decisions

## Components

- `main.py`: Main application interface
- `optimal_stopping.py`: Core simulation logic
- `utils.py`: Utility functions for data generation and statistics
