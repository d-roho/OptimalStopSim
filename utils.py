import numpy as np


def generate_sample_sequence(n_items, uniform_toggle=0):
    """
    Generate a sample sequence for visualization using normal distribution.

    Args:
        n_items (int): Number of items in the sequence

    Returns:
        np.array: Generated sequence with values clipped to [0,1]
    """
    sequence = np.clip(np.random.normal(0.5, 0.15, n_items), 0, 1)
    if uniform_toggle:
        sequence = np.random.uniform(0, 1, n_items)

    return sequence


def calculate_statistics(results):
    """
    Calculate statistics from simulation results.

    Args:
        results (pd.DataFrame): Simulation results

    Returns:
        dict: Dictionary containing calculated statistics
    """
    stats = {
        'success_rate': results['is_best'].mean(),
        'avg_position': results['position'].mean(),
        'best_value_rate':
        (results['value'] / results['best_possible']).mean(),
        'failure_rate': results['failure_to_find'].mean()
    }

    return stats
