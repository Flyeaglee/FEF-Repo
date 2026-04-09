
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
proxy = 'https://corsproxy.org/?'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("Fetching data through CORS proxy...")
url = proxy + target_url
response = requests.get(url, headers=headers, timeout=15)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

content = response.text

# Look for JSON data in the page
print("\n\nSearching for data structures...")

# Try to find JSON data in script tags
json_patterns = [
    r'window\.\_\_INITIAL_STATE\_\_\\s\*=\\s\*({.*?});?',
    r'window\.\_\_DATA\_\_\\s\*=\\s\*({.*?});?',
    r'"portfolio":\\s\*({.*?})\\s\*[},]',
    r'"subnets":\\s\*(\[.*?\])\\s\*[},]',
]

for pattern in json_patterns:
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        print(f"Found match with pattern: {pattern[:50]}...")
        print(f"Match length: {len(matches[0])}")
        break

# Look for __NEXT_DATA__
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content, re.DOTALL)
if next_data_match:
    print("\nFound __NEXT_DATA__ script")
    try:
        next_data = json.loads(next_data_match.group(1))
        print(f"Top-level keys: {list(next_data.keys())}")
        
        if 'props' in next_data and 'pageProps' in next_data['props']:
            page_props = next_data['props']['pageProps']
            print(f"\nPageProps keys: {list(page_props.keys())}")
            
            # Look for portfolio or subnet data
            for key in page_props.keys():
                value = page_props[key]
                if isinstance(value, (dict, list)) and len(str(value)) > 100:
                    print(f"\n--- Key: {key} ---")
                    print(f"Type: {type(value).__name__}, Size: {len(str(value))}")
                    if isinstance(value, dict):
                        print(f"Sub-keys: {list(value.keys())[:10]}")
                    elif isinstance(value, list) and len(value) > 0:
                        print(f"Items count: {len(value)}")
                        if isinstance(value[0], dict):
                            print(f"First item keys: {list(value[0].keys())}")
    except Exception as e:
        print(f"Error parsing: {e}")

# Look for table data or specific HTML structures
print("\n\nLooking for table structures...")
table_pattern = r'<table[^>]*>(.*?)</table>'
tables = re.findall(table_pattern, content, re.DOTALL | re.IGNORECASE)
print(f"Found {len(tables)} tables")

# Look for specific data patterns
print("\n\nSearching for subnet/balance patterns...")
subnet_patterns = [
    r'Subnet\\s\+\\d+[^<]{0,200}',
    r'\\d+\\.?\\d\*\\s\*TAO[^<]{0,100}',
    r'\\$[\\d,]+\\.?\\d\*[^<]{0,100}',
]

for pattern in subnet_patterns:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f"Pattern '{pattern[:30]}...' found {len(matches)} matches")
        for match in matches[:3]:
            print(f"  -> {match[:100]}")