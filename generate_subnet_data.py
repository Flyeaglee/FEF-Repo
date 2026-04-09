
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

# Set random seed for reproducibility
np.random.seed(42)

# Generate realistic Bittensor subnet data
# Based on known characteristics of Bittensor subnets

n_subnets = 45  # Current number of subnets

# Generate subnet IDs
subnet_ids = list(range(1, n_subnets + 1))

# Generate independent variables based on Bittensor network characteristics

# 1. Validator Count - More validators typically indicate more interest/activity
validator_count = np.random.poisson(lam=50, size=n_subnets) + np.random.randint(10, 100, n_subnets)
validator_count = np.clip(validator_count, 5, 500)

# 2. Miner Count - More miners = more compute power
miner_count = np.random.poisson(lam=200, size=n_subnets) + np.random.randint(50, 300, n_subnets)
miner_count = np.clip(miner_count, 20, 2000)

# 3. API Calls per Day - Network usage metric
api_calls_per_day = np.random.exponential(scale=50000, size=n_subnets) + np.random.randint(1000, 10000, n_subnets)
api_calls_per_day = np.clip(api_calls_per_day, 1000, 500000)

# 4. Total Stake (TAO) - Amount of TAO staked in the subnet
total_stake = np.random.lognormal(mean=8, sigma=1.5, size=n_subnets) * 1000
total_stake = np.clip(total_stake, 1000, 500000)

# 5. Network Activity Score - Composite metric of subnet activity
network_activity = np.random.beta(2, 5, n_subnets) * 100

# 6. Immunity Status (binary) - Whether subnet has immunity
immunity_status = np.random.choice([0, 1], size=n_subnets, p=[0.7, 0.3])

# 7. Pruning Rank - Lower is better (higher rank number = more likely to be pruned)
pruning_rank = np.random.randint(1, n_subnets + 1, n_subnets)

# 8. Ecosystem Routing - How much other subnets use this subnet
ecosystem_routing = np.random.exponential(scale=1000, size=n_subnets)
ecosystem_routing = np.clip(ecosystem_routing, 100, 50000)

# 9. Revenue per Validator - Economic incentive
revenue_per_validator = np.random.lognormal(mean=3, sigma=0.8, size=n_subnets)
revenue_per_validator = np.clip(revenue_per_validator, 1, 500)

# 10. Uptime Percentage - Reliability metric
uptime_percentage = np.random.beta(8, 2, n_subnets) * 100

# 11. Block Production Rate - How actively the subnet produces blocks
block_production_rate = np.random.normal(loc=0.8, scale=0.15, size=n_subnets)
block_production_rate = np.clip(block_production_rate, 0.3, 1.0)

# 12. Unique Miners - Diversity of miners
unique_miners = (miner_count * np.random.uniform(0.6, 0.95, n_subnets)).astype(int)

# 13. Delegation Count - Number of delegations
delegation_count = np.random.poisson(lam=100, size=n_subnets) + np.random.randint(10, 50, n_subnets)

# 14. Average Validator Stake
avg_validator_stake = total_stake / np.maximum(validator_count, 1) * np.random.uniform(0.8, 1.2, n_subnets)

# Create DataFrame
df = pd.DataFrame({
    'subnet_id': subnet_ids,
    'validator_count': validator_count,
    'miner_count': miner_count,
    'api_calls_per_day': api_calls_per_day,
    'total_stake': total_stake,
    'network_activity': network_activity,
    'immunity_status': immunity_status,
    'pruning_rank': pruning_rank,
    'ecosystem_routing': ecosystem_routing,
    'revenue_per_validator': revenue_per_validator,
    'uptime_percentage': uptime_percentage,
    'block_production_rate': block_production_rate,
    'unique_miners': unique_miners,
    'delegation_count': delegation_count,
    'avg_validator_stake': avg_validator_stake
})

print("Generated Bittensor Subnet Dataset")
print(f"Number of subnets: {len(df)}")
print(f"\nDataset Preview:")
print(df.head())
print(f"\nDataset Statistics:")
print(df.describe())

# Save the dataset
df.to_csv('bittensor_subnet_data.csv', index=False)
print("\nDataset saved to bittensor_subnet_data.csv")