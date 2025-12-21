"""
Utils for plotting, ...
"""

import matplotlib.pyplot as plt


def plot_regression(y_actual, y_predicted, set_name="Test"):
    """
    Plot actual vs predicted values for regression model.


    Args:
        y_actual: Actual quality values
        y_predicted: Predicted quality values
        set_name: Name of dataset (Train or Test)
    """
    plt.figure(figsize=(6, 4))

    plt.scatter(y_actual, y_predicted, alpha=0.6, s=50)

    min_val = min(y_actual.min(), y_predicted.min())
    max_val = max(y_actual.max(), y_predicted.max())
    plt.plot(
        [min_val, max_val], [min_val, max_val], "r-", linewidth=1.5, label="Perfect Fit"
    )

    plt.xlabel("Actual Quality", fontsize=12)
    plt.ylabel("Predicted Quality", fontsize=12)
    plt.title(f"{set_name} Set: Actual vs Predicted Quality", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()
