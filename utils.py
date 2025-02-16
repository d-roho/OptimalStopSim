import numpy as np


def generate_sample_sequence(n_items):
    """
    Generate a sample sequence for visualization using normal distribution.

    Args:
        n_items (int): Number of items in the sequence

    Returns:
        np.array: Generated sequence with values clipped to [0,1]
    """
    return np.clip(np.random.normal(0.5, 0.15, n_items), 0, 1)


def calculate_statistics(results):
    """
    Calculate statistics from simulation results.

    Args:
        results (pd.DataFrame): Simulation results

    Returns:
        dict: Dictionary containing calculated statistics
    """
    stats = {
        # Mean statistics
        'success_rate': results['is_best'].mean(),
        'avg_position': results['position'].mean(),
        'best_value_rate': (results['value'] / results['best_possible']).mean(),
        'failure_rate': results['failure_to_find'].mean(),

        # Median statistics
        'median_position': results['position'].median(),
        'median_value': results['value'].median(),
        'median_best_possible': results['best_possible'].median(),
        'median_value_rate': np.median(results['value'] / results['best_possible'])
    }

    return stats