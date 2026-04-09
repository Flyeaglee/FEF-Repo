
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

# Test accessing taostats subnets data
url = 'https://taostats.io/subnets'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    
    # Look for JSON data in the response
    content = response.text
    
    # Try to find subnet data structure
    if 'subnet' in content.lower():
        print("Found subnet references in content")
    
    # Look for price patterns
    price_pattern = r'\$[\d,]+\.?\d*'
    prices = re.findall(price_pattern, content)
    print(f"Found {len(prices)} price values")
    if prices:
        print(f"Sample prices: {prices[:5]}")
        
    # Look for emission patterns
    emission_pattern = r'[\d,]+\.?\d*\s*TAO'
    emissions = re.findall(emission_pattern, content)
    print(f"Found {len(emissions)} emission values")
    if emissions:
        print(f"Sample emissions: {emissions[:5]}")
        
    # Look for JSON structures
    json_matches = re.findall(r'\{[^{}]{50,5000}\}', content)
    print(f"Found {len(json_matches)} potential JSON objects")
    
    if json_matches:
        # Try to parse a few to see structure
        for i, match in enumerate(json_matches[:3]):
            try:
                data = json.loads(match)
                if isinstance(data, dict) and ('subnet' in str(data).lower() or 'name' in data or 'id' in data):
                    print(f"JSON {i+1} contains subnet data: {str(data)[:200]}")
                    break
            except:
                pass
                
except Exception as e:
    print(f"Error: {e}")