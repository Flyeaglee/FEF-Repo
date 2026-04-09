
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

url = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
content = response.text

# Look for fetch or axios calls
print("Looking for fetch/axios calls...")
fetch_patterns = [
    r'fetch\([\'\"]([^\'\"]+)[\'\"]',
    r'axios\.[get|post|put|delete]+\([\'\"]([^\'\"]+)[\'\"]',
    r'url:\s*[\'\"]([^\'\"]*(?:api|portfolio|subnet)[^\'\"]*)[\'\"]',
    r'/api/[^\'\"\s\>\<]+',
]

for pattern in fetch_patterns:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f"Pattern matched: {pattern[:40]}...")
        unique_matches = list(set(matches))[:10]
        for match in unique_matches:
            print(f"  -> {match[:100]}")

# Look for specific taostats API patterns
print("\n\nLooking for taostats-specific patterns...")
tao_patterns = [
    r'taostats\.io/api/[^\'\"\s\>\<]+',
    r'api\.taostats\.io[^\'\"\s\>\<]+',
    r'/api/portfolio[^\'\"\s\>\<]*',
    r'/api/subnet[^\'\"\s\>\<]*',
]

for pattern in tao_patterns:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f"Found: {matches[:5]}")

# Try to find the wallet address usage
print("\n\nLooking for wallet address in scripts...")
wallet = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
if wallet in content:
    # Find context around wallet address
    idx = content.find(wallet)
    context = content[max(0, idx-200):min(len(content), idx+200)]
    print(f"Context around wallet: ...{context}...")