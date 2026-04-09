
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

# Try more CORS proxies
wallet = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
target_url = f'https://taostats.io/pro/portfolio/{wallet}'

more_proxies = [
    'https://thingproxy.freeboard.io/fetch/',
    'https://corsproxy.org/?',
    'https://api.codetabs.com/v1/proxy?quest=',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("Testing more CORS proxies...")
for proxy in more_proxies:
    try:
        url = proxy + target_url
        print(f"\nTrying: {proxy}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  Content length: {len(response.text)}")
            if len(response.text) > 1000:
                print("  -> Got substantial content!")
    except Exception as e:
        print(f"  Error: {str(e)[:100]}")