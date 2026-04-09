
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


# Comprehensive test of the full implementation
import subprocess
import time
import requests
import sys
import signal
import os
import json

print("=" * 60)
print("COMPREHENSIVE IMPLEMENTATION TEST")
print("=" * 60)

# Start the proxy server
print("\n[1/5] Starting proxy server...")
server_process = subprocess.Popen(
    [sys.executable, 'proxy_server.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    preexec_fn=os.setsid
)
time.sleep(4)

try:
    # Test 1: Health endpoint
    print("\n[2/5] Testing health endpoint...")
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    data = response.json()
    assert data['status'] == 'ok', "Health status not ok"
    print("✓ Health endpoint working")
    
    # Test 2: Portfolio endpoint
    print("\n[3/5] Testing portfolio endpoint...")
    response = requests.get('http://localhost:5000/api/portfolio', timeout=15)
    assert response.status_code == 200, f"Portfolio endpoint failed: {response.status_code}"
    data = response.json()
    assert 'success' in data, "Missing success field"
    assert 'source' in data, "Missing source field"
    print(f"✓ Portfolio endpoint working (source: {data['source']})")
    
    # Test 3: Verify index.html exists and has correct structure
    print("\n[4/5] Verifying frontend files...")
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    assert 'Devin\'s Subnet Holdings' in html_content, "Missing title"
    assert '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ' in html_content, "Missing wallet address"
    assert 'PROXY_URL' in html_content, "Missing PROXY_URL"
    assert 'fetch(PROXY_URL)' in html_content, "Not using PROXY_URL for fetch"
    assert 'dark' in html_content.lower() or '#0d1117' in html_content, "Missing dark mode styling"
    print("✓ index.html structure correct")
    
    # Test 4: Verify proxy_server.py exists and is valid
    print("\n[5/5] Verifying backend files...")
    with open('proxy_server.py', 'r') as f:
        proxy_content = f.read()
    
    assert 'Flask' in proxy_content, "Flask not imported"
    assert '/api/portfolio' in proxy_content, "Missing portfolio endpoint"
    assert 'taostats.io' in proxy_content, "Missing taostats.io reference"
    print("✓ proxy_server.py structure correct")
    
    # Test 5: Verify requirements.txt
    with open('requirements.txt', 'r') as f:
        req_content = f.read()
    assert 'flask' in req_content.lower(), "Flask not in requirements"
    assert 'requests' in req_content.lower(), "Requests not in requirements"
    print("✓ requirements.txt correct")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print("\nImplementation Summary:")
    print("- Backend proxy server: Running on port 5000")
    print("- Frontend: index.html with dark mode UI")
    print("- Data fetching: Uses PROXY_URL to bypass CORS")
    print("- Error handling: Graceful fallback for auth requirements")
    
except AssertionError as e:
    print(f"\n✗ TEST FAILED: {e}")
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print("\nStopping proxy server...")
    try:
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    except:
        server_process.terminate()
    server_process.wait()
    print("Cleanup complete")