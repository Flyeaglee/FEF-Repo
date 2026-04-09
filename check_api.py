
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

# Check if taostats.io has a direct API
url = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
try:
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Content type: {response.headers.get('content-type')}"[:100])
    # Check if there's JSON data available
    if 'application/json' in response.headers.get('content-type', ''):
        print("JSON response found!")
        print(response.json()[:200] if response.text else "Empty response")
    else:
        print("Not a JSON response. Looking for API endpoints...")
        # Look for API patterns in the HTML
        content = response.text
        if 'api' in content.lower():
            print("Found 'api' references in the page")
        if 'json' in content.lower():
            print("Found 'json' references in the page")
except Exception as e:
    print(f"Error: {e}")