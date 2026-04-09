
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

wallet = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
target_url = f'https://taostats.io/pro/portfolio/{wallet}'
proxy = 'https://api.codetabs.com/v1/proxy?quest='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("Fetching data through codetabs CORS proxy...")
url = proxy + target_url
response = requests.get(url, headers=headers, timeout=20)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

content = response.text

# Save a sample of the content for analysis
with open('sample_content.txt', 'w', encoding='utf-8') as f:
    f.write(content[:50000])  # First 50KB
print("Saved first 50KB to sample_content.txt")

# Check for key indicators
print("\n\nChecking content...")
print(f"Contains 'subnet': {'subnet' in content.lower()}")
print(f"Contains 'portfolio': {'portfolio' in content.lower()}")
print(f"Contains '__NEXT_DATA__': {'__NEXT_DATA__' in content}")
print(f"Contains 'login': {'login' in content.lower()}")

# Look for the first 500 chars
print("\n\nFirst 1000 characters:")
print(content[:1000])