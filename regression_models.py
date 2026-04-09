
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
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('bittensor_subnet_data.csv')

# Define independent variables for both models
independent_vars = [
    'validator_count', 'miner_count', 'api_calls_per_day', 'total_stake',
    'network_activity', 'immunity_status', 'pruning_rank', 'ecosystem_routing',
    'revenue_per_validator', 'uptime_percentage', 'block_production_rate',
    'unique_miners', 'delegation_count', 'avg_validator_stake'
]

# Prepare data
X = df[independent_vars]
y_price = df['subnet_price']
y_emissions = df['emissions_tao']

# Add constant for intercept
X_const = sm.add_constant(X)

print("=" * 80)
print("BITTENSOR SUBNET REGRESSION ANALYSIS")
print("=" * 80)

# ============================================================
# MODEL 1: SUBNET PRICE REGRESSION
# ============================================================
print("\n" + "=" * 80)
print("MODEL 1: MULTIPLE LINEAR REGRESSION - SUBNET PRICE DRIVERS")
print("=" * 80)

model_price = sm.OLS(y_price, X_const).fit()
print(model_price.summary())

# Calculate VIF for multicollinearity check
vif_data = pd.DataFrame()
vif_data["Variable"] = independent_vars
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print("\n\nVariance Inflation Factors (VIF) - Multicollinearity Check:")
print(vif_data.to_string(index=False))

# Model diagnostics for price model
print("\n\nModel Diagnostics - Subnet Price:")
print(f"R-squared: {model_price.rsquared:.4f}")
print(f"Adjusted R-squared: {model_price.rsquared_adj:.4f}")
print(f"F-statistic: {model_price.fvalue:.4f}")
print(f"Prob (F-statistic): {model_price.f_pvalue:.2e}")
print(f"AIC: {model_price.aic:.2f}")
print(f"BIC: {model_price.bic:.2f}")

# Breusch-Pagan test for heteroscedasticity
bp_test = het_breuschpagan(model_price.resid, X_const)
print(f"\nBreusch-Pagan Test (Heteroscedasticity):")
print(f"  LM Statistic: {bp_test[0]:.4f}")
print(f"  LM p-value: {bp_test[1]:.4f}")

# ============================================================
# MODEL 2: EMISSIONS REGRESSION
# ============================================================
print("\n" + "=" * 80)
print("MODEL 2: MULTIPLE LINEAR REGRESSION - EMISSION DRIVERS")
print("=" * 80)

model_emissions = sm.OLS(y_emissions, X_const).fit()
print(model_emissions.summary())

# Model diagnostics for emissions model
print("\n\nModel Diagnostics - Emissions:")
print(f"R-squared: {model_emissions.rsquared:.4f}")
print(f"Adjusted R-squared: {model_emissions.rsquared_adj:.4f}")
print(f"F-statistic: {model_emissions.fvalue:.4f}")
print(f"Prob (F-statistic): {model_emissions.f_pvalue:.2e}")
print(f"AIC: {model_emissions.aic:.2f}")
print(f"BIC: {model_emissions.bic:.2f}")

# Breusch-Pagan test for heteroscedasticity
bp_test_2 = het_breuschpagan(model_emissions.resid, X_const)
print(f"\nBreusch-Pagan Test (Heteroscedasticity):")
print(f"  LM Statistic: {bp_test_2[0]:.4f}")
print(f"  LM p-value: {bp_test_2[1]:.4f}")

# Save model results
results_summary = {
    'price_model': {
        'r_squared': model_price.rsquared,
        'adj_r_squared': model_price.rsquared_adj,
        'f_statistic': model_price.fvalue,
        'f_pvalue': model_price.f_pvalue,
        'aic': model_price.aic,
        'bic': model_price.bic
    },
    'emissions_model': {
        'r_squared': model_emissions.rsquared,
        'adj_r_squared': model_emissions.rsquared_adj,
        'f_statistic': model_emissions.fvalue,
        'f_pvalue': model_emissions.f_pvalue,
        'aic': model_emissions.aic,
        'bic': model_emissions.bic
    }
}

print("\n\nModel results computed successfully!")