
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

# Try to find public Bittensor/TAO APIs
apis_to_try = [
    # Taostats public endpoints
    ('Taostats subnets', 'https://taostats.io/subnets'),
    ('Taostats API', 'https://taostats.io/api/subnets'),
    
    # Alternative Bittensor explorers
    ('Bittensor API', 'https://api.bittensor.com/'),
    
    # Subscan (blockchain explorer)
    ('Subscan Bittensor', 'https://bittensor.api.subscan.io/api/scan/metadata'),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/json',
}

print("Testing alternative data sources...")
for name, url in apis_to_try:
    try:
        print(f"\n{name}: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            print(f"  Content-Type: {content_type}")
            if 'json' in content_type:
                try:
                    data = response.json()
                    print(f"  JSON keys: {list(data.keys())[:5] if isinstance(data, dict) else 'N/A'}")
                except:
                    print(f"  Response: {response.text[:200]}")
            else:
                print(f"  HTML length: {len(response.text)}")
    except Exception as e:
        print(f"  Error: {str(e)[:100]}")