
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


# Start the proxy server in background and test
import subprocess
import time
import requests
import sys

print("Starting proxy server...")
# Start the server
server_process = subprocess.Popen(
    [sys.executable, 'proxy_server.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(3)

try:
    # Test health endpoint
    print("\nTesting health endpoint...")
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test portfolio endpoint
    print("\nTesting portfolio endpoint...")
    response = requests.get('http://localhost:5000/api/portfolio', timeout=15)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Source: {data.get('source')}")
    print(f"Message: {data.get('message', 'N/A')[:100]}")
    
finally:
    # Clean up
    print("\nStopping proxy server...")
    server_process.terminate()
    server_process.wait()