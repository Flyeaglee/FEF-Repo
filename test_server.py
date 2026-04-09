
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


import subprocess
import time
import requests
import sys
import signal
import os

# Start the proxy server
print("Starting proxy server...")
server_process = subprocess.Popen(
    [sys.executable, 'proxy_server.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    preexec_fn=os.setsid  # Create new process group
)

# Wait for server to start
time.sleep(4)

try:
    # Test health endpoint
    print("\n=== Testing Health Endpoint ===")
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test portfolio endpoint
    print("\n=== Testing Portfolio Endpoint ===")
    response = requests.get('http://localhost:5000/api/portfolio', timeout=15)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Source: {data.get('source')}")
    print(f"Message: {data.get('message', 'N/A')[:100]}...")
    print(f"Data items: {len(data.get('data', []))}")
    
    print("\n=== All tests passed! ===")
    
except Exception as e:
    print(f"\nError: {e}")
    # Print server output for debugging
    stdout, stderr = server_process.communicate(timeout=2)
    print(f"Server stdout: {stdout.decode()[:500] if stdout else 'None'}"  )
    print(f"Server stderr: {stderr.decode()[:500] if stderr else 'None'}"  )
    
finally:
    # Clean up - kill the entire process group
    print("\nStopping proxy server...")
    try:
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    except:
        server_process.terminate()
    server_process.wait()