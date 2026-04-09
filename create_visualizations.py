
import sys, pytest, collections, collections.abc, urllib3.exceptions, _pytest.pytester, numpy;
collections.Mapping = collections.abc.Mapping;
collections.MutableMapping = collections.abc.MutableMapping;
collections.MutableSet = collections.abc.MutableSet;
collections.Sequence = collections.abc.Sequence;
collections.Callable = collections.abc.Callable;
collections.Iterable = collections.abc.Iterable;
collections.Iterator = collections.abc.Iterator;
urllib3.exceptions.SNIMissingWarning = urllib3.exceptions.DependencyWarning;
pytest.RemovedInPytest4Warning = DeprecationWarning;
_pytest.pytester.Testdir = _pytest.pytester.Pytester;
numpy.PINF = numpy.inf;
numpy.unicode_ = numpy.str_;
numpy.bytes_ = numpy.bytes_;
numpy.float_ = numpy.float64;
numpy.string_ = numpy.bytes_;
numpy.NaN = numpy.nan;


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('bittensor_subnet_data.csv')

# Prepare data for models
independent_vars = [
    'validator_count', 'miner_count', 'api_calls_per_day', 'total_stake',
    'network_activity', 'immunity_status', 'pruning_rank', 'ecosystem_routing',
    'revenue_per_validator', 'uptime_percentage', 'block_production_rate',
    'unique_miners', 'delegation_count', 'avg_validator_stake'
]

X = df[independent_vars]
X_const = sm.add_constant(X)
y_price = df['subnet_price']
y_emissions = df['emissions_tao']

# Fit models
model_price = sm.OLS(y_price, X_const).fit()
model_emissions = sm.OLS(y_emissions, X_const).fit()

# Create visualizations

# 1. Actual vs Predicted for both models
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Price model
y_price_pred = model_price.predict(X_const)
axes[0].scatter(y_price, y_price_pred, alpha=0.7, color='blue')
axes[0].plot([y_price.min(), y_price.max()], [y_price.min(), y_price.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Price')
axes[0].set_ylabel('Predicted Price')
axes[0].set_title('Subnet Price: Actual vs Predicted\n(R² = {:.3f})'.format(model_price.rsquared))
axes[0].grid(True, alpha=0.3)

# Emissions model
y_emissions_pred = model_emissions.predict(X_const)
axes[1].scatter(y_emissions, y_emissions_pred, alpha=0.7, color='green')
axes[1].plot([y_emissions.min(), y_emissions.max()], [y_emissions.min(), y_emissions.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Emissions')
axes[1].set_ylabel('Predicted Emissions')
axes[1].set_title('Emissions: Actual vs Predicted\n(R² = {:.3f})'.format(model_emissions.rsquared))
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Residual plots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Price model residuals
residuals_price = model_price.resid
axes[0].scatter(y_price_pred, residuals_price, alpha=0.7, color='blue')
axes[0].axhline(y=0, color='r', linestyle='--')
axes[0].set_xlabel('Predicted Price')
axes[0].set_ylabel('Residuals')
axes[0].set_title('Subnet Price: Residual Plot')
axes[0].grid(True, alpha=0.3)

# Emissions model residuals
residuals_emissions = model_emissions.resid
axes[1].scatter(y_emissions_pred, residuals_emissions, alpha=0.7, color='green')
axes[1].axhline(y=0, color='r', linestyle='--')
axes[1].set_xlabel('Predicted Emissions')
axes[1].set_ylabel('Residuals')
axes[1].set_title('Emissions: Residual Plot')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('residual_plots.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Feature importance plots
# Get significant coefficients for each model (p < 0.05)
price_coef = model_price.params[1:]  # Exclude intercept
price_pvalues = model_price.pvalues[1:]

emissions_coef = model_emissions.params[1:]  # Exclude intercept
emissions_pvalues = model_emissions.pvalues[1:]

# Filter significant coefficients
price_sig_coef = price_coef[price_pvalues < 0.05]
emissions_sig_coef = emissions_coef[emissions_pvalues < 0.05]

# Plot significant coefficients
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

if len(price_sig_coef) > 0:
    price_sig_coef.sort_values().plot(kind='barh', ax=axes[0], color='skyblue')
    axes[0].set_title('Significant Price Drivers (p < 0.05)')
    axes[0].set_xlabel('Coefficient Value')
    axes[0].grid(True, alpha=0.3)
else:
    axes[0].text(0.5, 0.5, 'No significant coefficients\n(p < 0.05)', ha='center', va='center', transform=axes[0].transAxes)
    axes[0].set_title('Significant Price Drivers (p < 0.05)')

if len(emissions_sig_coef) > 0:
    emissions_sig_coef.sort_values().plot(kind='barh', ax=axes[1], color='lightgreen')
    axes[1].set_title('Significant Emission Drivers (p < 0.05)')
    axes[1].set_xlabel('Coefficient Value')
    axes[1].grid(True, alpha=0.3)
else:
    axes[1].text(0.5, 0.5, 'No significant coefficients\n(p < 0.05)', ha='center', va='center', transform=axes[1].transAxes)
    axes[1].set_title('Significant Emission Drivers (p < 0.05)')

plt.tight_layout()
plt.savefig('significant_coefficients.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Distribution plots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

axes[0].hist(y_price, bins=15, alpha=0.7, color='blue', edgecolor='black')
axes[0].set_xlabel('Subnet Price')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Subnet Prices')
axes[0].grid(True, alpha=0.3)

axes[1].hist(y_emissions, bins=15, alpha=0.7, color='green', edgecolor='black')
axes[1].set_xlabel('Emissions (TAO)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution of Emissions')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizations created successfully!")