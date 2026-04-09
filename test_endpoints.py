
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

# Try different potential API endpoints
wallet = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'

endpoints_to_try = [
    f'https://taostats.io/api/portfolio/{wallet}',
    f'https://api.taostats.io/portfolio/{wallet}',
    f'https://taostats.io/api/v1/portfolio/{wallet}',
    f'https://taostats.io/api/wallet/{wallet}',
    f'https://taostats.io/api/account/{wallet}',
    'https://taostats.io/api/subnets',
    'https://api.taostats.io/subnets',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

print("Testing API endpoints...")
for endpoint in endpoints_to_try:
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"\n{endpoint}")
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'json' in content_type:
                try:
                    data = response.json()
                    print(f"  JSON Response: {json.dumps(data, indent=2)[:500]}")
                except:
                    print(f"  Response: {response.text[:200]}")
            else:
                print(f"  Response preview: {response.text[:200]}")
    except Exception as e:
        print(f"\n{endpoint}")
        print(f"  Error: {e}")