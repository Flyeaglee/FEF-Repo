
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


# Test the frontend JavaScript logic
# This simulates what the browser would do

import requests
import json

print("Testing Frontend-Backend Integration")
print("=" * 50)

# Simulate the frontend fetch to the proxy
PROXY_URL = 'http://localhost:5000/api/portfolio'

print(f"\nFetching from: {PROXY_URL}")

try:
    response = requests.get(PROXY_URL, timeout=10)
    print(f"Response status: {response.status_code}")
    
    result = response.json()
    print(f"\nResponse structure:")
    print(f"  - success: {result.get('success')}")
    print(f"  - source: {result.get('source')}")
    print(f"  - has message: {'message' in result}")
    print(f"  - data items: {len(result.get('data', []))}")
    
    # Simulate transformData function
    def transformData(data):
        if not isinstance(data, list):
            return []
        return [{
            'subnetName': item.get('subnetName', item.get('name', f"Subnet {item.get('subnetId', item.get('id', 'Unknown'))}")),
            'balance': item.get('balance', item.get('amount', '0 TAO')),
            'currentPrice': item.get('currentPrice', item.get('price', item.get('value', '$0.00')))
        } for item in data]
    
    if result.get('success'):
        if result.get('data') and len(result['data']) > 0:
            transformed = transformData(result['data'])
            print(f"\nTransformed data sample:")
            for item in transformed[:3]:
                print(f"  - {item['subnetName']}: {item['balance']} @ {item['currentPrice']}")
        elif result.get('message'):
            print(f"\nInfo message: {result['message'][:80]}...")
    
    print("\n✓ Frontend-Backend integration test passed")
    
except Exception as e:
    print(f"\n✗ Test failed: {e}")
    print("Note: Proxy server must be running for this test")