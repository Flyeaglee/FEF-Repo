
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


# Test the proxy server
import requests
import json

# Test the health endpoint
print("Testing health endpoint...")
try:
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"Health check status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")
    print("Proxy server may not be running yet")

# Test the portfolio endpoint
print("\nTesting portfolio endpoint...")
try:
    response = requests.get('http://localhost:5000/api/portfolio', timeout=10)
    print(f"Portfolio endpoint status: {response.status_code}")
    data = response.json()
    print(f"Response keys: {list(data.keys())}")
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Data source: {data.get('source')}")
        print(f"Data items: {len(data.get('data', []))}")
    else:
        print(f"Error: {data.get('error')}")
        print(f"Requires auth: {data.get('requiresAuth')}")
except Exception as e:
    print(f"Portfolio endpoint failed: {e}")