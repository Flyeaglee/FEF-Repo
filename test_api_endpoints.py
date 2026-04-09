
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

# Try direct API endpoints for taostats
api_endpoints = [
    'https://taostats.io/api/subnets',
    'https://api.taostats.io/subnets',
    'https://taostats.io/api/v1/subnets',
    'https://api.taostats.io/api/v1/subnets',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

for endpoint in api_endpoints:
    try:
        print(f"\nTrying {endpoint}")
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            print(f"Content-Type: {content_type}")
            
            if 'json' in content_type.lower():
                try:
                    data = response.json()
                    print(f"Successfully got JSON data")
                    if isinstance(data, list):
                        print(f"Got list with {len(data)} items")
                        if len(data) > 0:
                            print(f"Sample item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
                    elif isinstance(data, dict):
                        print(f"Got dict with keys: {list(data.keys())}")
                        # Look for data in common keys
                        for key in ['data', 'subnets', 'result', 'items']:
                            if key in data and isinstance(data[key], list):
                                print(f"Found '{key}' with {len(data[key])} items")
                                if len(data[key]) > 0:
                                    print(f"Sample item: {data[key][0]}")
                    break
                except Exception as e:
                    print(f"Error parsing JSON: {e}")
                    print(f"Response text sample: {response.text[:200]}")
            else:
                print(f"Non-JSON response, length: {len(response.text)}")
                print(f"Text sample: {response.text[:200]}")
        else:
            print(f"Non-200 status: {response.status_code}")
            if response.status_code in [403, 401]:
                print("Access denied - might need authentication or different headers")
                
    except Exception as e:
        print(f"Request failed: {e}")