
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


import requests
import re
import json

# Try to access taostats subnets page via CORS proxy
proxy = 'https://api.codetabs.com/v1/proxy?quest='
url = proxy + 'https://taostats.io/subnets'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("Fetching subnets page...")
response = requests.get(url, headers=headers, timeout=20)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

content = response.text

# Look for subnet data
print("\nSearching for subnet data...")

# Look for price data
price_pattern = r'\$[\d,]+\.?\d*'
prices = re.findall(price_pattern, content)
if prices:
    print(f"Found {len(prices)} price values")
    print(f"Sample prices: {prices[:10]}")

# Look for subnet numbers
subnet_pattern = r'Subnet\s+(\d+)'
subnets = re.findall(subnet_pattern, content)
if subnets:
    print(f"\nFound {len(subnets)} subnet references")
    print(f"Subnets: {sorted(set(subnets), key=int)[:20]}")

# Look for JSON data
print("\nLooking for JSON data structures...")
json_matches = re.findall(r'>({[\s\S]{500,10000}?})</script>', content)
print(f"Found {len(json_matches)} potential JSON blocks")

for i, match in enumerate(json_matches[:2]):
    print(f"\nJSON block {i+1} length: {len(match)}")
    try:
        data = json.loads(match)
        print(f"  Parsed! Type: {type(data).__name__}")
        if isinstance(data, dict):
            print(f"  Keys: {list(data.keys())[:10]}")
    except Exception as e:
        print(f"  Not valid JSON: {str(e)[:50]}")