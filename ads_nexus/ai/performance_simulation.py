import numpy as np

class PerformanceSimulation:
    def __init__(self, ad_data):
        self.ad_data = ad_data

    def simulate_performance(self, budget, targeting, schedule):
        # Simple linear regression-like simulation of performance
        # based on budget, targeting, and schedule
        performance_score = (budget * 0.5) + (targeting * 0.3) + (schedule * 0.2)
        return performance_score
