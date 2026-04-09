
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
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Load the generated data
df = pd.read_csv('bittensor_subnet_data.csv')

# Generate dependent variables with realistic relationships

# MODEL 1: SUBNET PRICE
# Price is driven by:
# - Total stake (positive - more stake = higher value)
# - Network activity (positive - more activity = higher demand)
# - API calls (positive - more usage = higher value)
# - Validator count (positive - more validators = more confidence)
# - Immunity status (positive - protected subnets have higher value)
# - Uptime (positive - reliability increases value)
# - Ecosystem routing (positive - more routing = higher value)

price_base = 0.5
price = (
    price_base +
    0.00001 * df['total_stake'] +
    0.005 * df['network_activity'] +
    0.000001 * df['api_calls_per_day'] +
    0.002 * df['validator_count'] +
    0.1 * df['immunity_status'] +
    0.003 * df['uptime_percentage'] +
    0.00001 * df['ecosystem_routing'] +
    np.random.normal(0, 0.3, len(df))  # Add noise
)
price = np.maximum(price, 0.1)  # Ensure positive prices
df['subnet_price'] = price

# MODEL 2: EMISSIONS
# Emissions are driven by:
# - Total stake (positive - more stake = more emissions)
# - Block production rate (positive - more blocks = more emissions)
# - Network activity (positive - more activity = more emissions)
# - Miner count (positive - more miners = more emissions)
# - Revenue per validator (positive - economic activity drives emissions)
# - Pruning rank (negative - higher rank = less emissions)
# - Unique miners (positive - diversity drives emissions)

emission_base = 50
emissions = (
    emission_base +
    0.0005 * df['total_stake'] +
    30 * df['block_production_rate'] +
    0.2 * df['network_activity'] +
    0.05 * df['miner_count'] +
    0.5 * df['revenue_per_validator'] -
    0.3 * df['pruning_rank'] +
    0.02 * df['unique_miners'] +
    np.random.normal(0, 5, len(df))  # Add noise
)
emissions = np.maximum(emissions, 10)  # Ensure positive emissions
df['emissions_tao'] = emissions

print("Dependent Variables Created")
print(f"\nSubnet Price Statistics:")
print(df['subnet_price'].describe())
print(f"\nEmissions Statistics:")
print(df['emissions_tao'].describe())

# Save updated dataset
df.to_csv('bittensor_subnet_data.csv', index=False)

# Display correlation matrix
correlation_vars = ['subnet_price', 'emissions_tao', 'validator_count', 'miner_count', 
                    'api_calls_per_day', 'total_stake', 'network_activity', 
                    'ecosystem_routing', 'revenue_per_validator', 'uptime_percentage']
corr_matrix = df[correlation_vars].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Matrix: Subnet Price and Emissions Drivers', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nCorrelation matrix saved to correlation_matrix.png")