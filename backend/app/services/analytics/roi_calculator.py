"""
ROI Calculation Engine
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from scipy import stats


class ROICalculator:
    """
    Calculate ROI for AI tools based on usage and productivity metrics
    """

    def __init__(self):
        pass

    def calculate_productivity_gain(
        self,
        baseline_metrics: List[Dict],
        current_metrics: List[Dict],
        metric_type: str
    ) -> Dict:
        """
        Calculate productivity gain comparing baseline to current metrics

        Args:
            baseline_metrics: Historical metrics before AI adoption
            current_metrics: Current metrics with AI usage
            metric_type: Type of metric being measured

        Returns:
            Dictionary with productivity gain statistics
        """
        baseline_df = pd.DataFrame(baseline_metrics)
        current_df = pd.DataFrame(current_metrics)

        # Calculate mean values
        baseline_mean = baseline_df['value'].mean()
        current_mean = current_df['value'].mean()

        # Calculate percentage change
        pct_change = ((current_mean - baseline_mean) / baseline_mean) * 100

        # Statistical significance test (t-test)
        t_stat, p_value = stats.ttest_ind(baseline_df['value'], current_df['value'])

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((baseline_df['value'].std()**2 + current_df['value'].std()**2) / 2)
        cohens_d = (current_mean - baseline_mean) / pooled_std if pooled_std > 0 else 0

        return {
            'baseline_mean': baseline_mean,
            'current_mean': current_mean,
            'absolute_change': current_mean - baseline_mean,
            'percentage_change': pct_change,
            'p_value': p_value,
            'is_significant': p_value < 0.05,
            'effect_size': cohens_d,
            'sample_size_baseline': len(baseline_df),
            'sample_size_current': len(current_df),
        }

    def calculate_ai_tool_roi(
        self,
        ai_tool_cost: float,
        productivity_gains: Dict,
        employee_cost_per_hour: float,
        time_period_days: int = 30
    ) -> Dict:
        """
        Calculate ROI for an AI tool

        Args:
            ai_tool_cost: Monthly cost of the AI tool
            productivity_gains: Output from calculate_productivity_gain
            employee_cost_per_hour: Loaded cost of employee per hour
            time_period_days: Time period for calculation

        Returns:
            Dictionary with ROI metrics
        """
        # Calculate value of productivity gains
        # Assuming productivity improvement translates to time saved
        hours_per_month = 160  # Standard work month
        time_saved_pct = productivity_gains['percentage_change'] / 100

        # Calculate monetary value of time saved
        time_saved_hours = hours_per_month * time_saved_pct
        value_of_time_saved = time_saved_hours * employee_cost_per_hour

        # Calculate ROI
        net_benefit = value_of_time_saved - ai_tool_cost
        roi_percentage = (net_benefit / ai_tool_cost) * 100 if ai_tool_cost > 0 else 0

        # Calculate payback period in months
        payback_months = ai_tool_cost / value_of_time_saved if value_of_time_saved > 0 else float('inf')

        return {
            'ai_tool_cost': ai_tool_cost,
            'value_generated': value_of_time_saved,
            'net_benefit': net_benefit,
            'roi_percentage': roi_percentage,
            'payback_period_months': payback_months,
            'time_saved_hours_per_month': time_saved_hours,
            'is_positive_roi': roi_percentage > 0,
        }

    def calculate_fte_equivalent(
        self,
        total_time_saved_hours: float,
        hours_per_fte: float = 2080  # Annual hours
    ) -> float:
        """
        Calculate FTE equivalent of time saved

        Args:
            total_time_saved_hours: Total hours saved
            hours_per_fte: Hours per FTE (default: 2080 = 52 weeks * 40 hours)

        Returns:
            FTE equivalent
        """
        return total_time_saved_hours / hours_per_fte


# Example usage (commented out):
"""
calculator = ROICalculator()

# Example baseline and current metrics
baseline = [{'value': 45}, {'value': 50}, {'value': 48}]  # Minutes to complete task
current = [{'value': 30}, {'value': 32}, {'value': 28}]  # With AI assistance

# Calculate productivity gain
productivity_gain = calculator.calculate_productivity_gain(baseline, current, 'task_completion_time')

# Calculate ROI
roi = calculator.calculate_ai_tool_roi(
    ai_tool_cost=15000,  # $15K per month
    productivity_gains=productivity_gain,
    employee_cost_per_hour=75,  # $75/hour loaded cost
    time_period_days=30
)

print(roi)
"""
