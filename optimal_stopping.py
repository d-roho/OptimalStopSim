import numpy as np
import pandas as pd

def simulate_optimal_stopping(n_items, n_simulations, look_ratio):
    """
    Simulate the optimal stopping problem multiple times.
    
    Args:
        n_items (int): Number of items in each sequence
        n_simulations (int): Number of simulations to run
        look_ratio (float): Proportion of items to observe before making a decision
    
    Returns:
        pd.DataFrame: Results of all simulations
    """
    results = []
    
    for _ in range(n_simulations):
        # Generate random sequence
        sequence = np.random.uniform(0, 1, n_items)
        
        # Calculate looking phase length
        look_phase = int(n_items * look_ratio)
        
        # Find maximum value in looking phase
        look_max = np.max(sequence[:look_phase]) if look_phase > 0 else -np.inf
        
        # Selection phase
        selected_pos = n_items - 1  # Default to last position
        selected_value = sequence[selected_pos]
        
        for i in range(look_phase, n_items):
            if sequence[i] > look_max:
                selected_pos = i
                selected_value = sequence[i]
                break
        
        # Record results
        results.append({
            'position': selected_pos,
            'value': selected_value,
            'is_best': selected_value == np.max(sequence),
            'best_possible': np.max(sequence)
        })
    
    return pd.DataFrame(results)
