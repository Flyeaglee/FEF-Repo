
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
import json
import re

# Try using a CORS proxy to access taostats
proxy = 'https://api.codetabs.com/v1/proxy?quest='
url = proxy + 'https://taostats.io/subnets'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    content = response.text
    
    # Look for fetch/XHR calls in the JavaScript
    print("Looking for API calls in JavaScript...")
    
    # Look for fetch calls
    fetch_pattern = r'fetch\([\'"]([^\'"]+)[\'"]'
    fetches = re.findall(fetch_pattern, content)
    print(f"Found {len(fetches)} fetch calls")
    for f in fetches[:10]:
        print(f"  {f}")
    
    # Look for axios or other HTTP client calls
    axios_pattern = r'axios\.(get|post)\([\'"]([^\'"]+)[\'"]'
    axios_calls = re.findall(axios_pattern, content)
    print(f"\nFound {len(axios_calls)} axios calls")
    for method, endpoint in axios_calls[:10]:
        print(f"  {method.upper()}: {endpoint}")
    
    # Look for API endpoint patterns
    api_pattern = r'["\']([^"\']*api[^"\']*)["\']'
    api_matches = re.findall(api_pattern, content, re.IGNORECASE)
    print(f"\nFound {len(api_matches)} API-related strings")
    unique_apis = list(set(api_matches))[:20]
    for api in unique_apis:
        if len(api) > 10 and 'taostats' in api.lower():
            print(f"  {api}")
    
    # Look for GraphQL queries
    graphql_pattern = r'query\s+\w+\s*\{'
    graphql_matches = re.findall(graphql_pattern, content)
    print(f"\nFound {len(graphql_matches)} GraphQL query patterns")
    
    # Look for specific data loading patterns
    data_pattern = r'["\'](subnets|subnet|price|emission|validator)["\']\s*:\s*'
    data_matches = re.findall(data_pattern, content, re.IGNORECASE)
    print(f"\nFound {len(data_matches)} data field references")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()