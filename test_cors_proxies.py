
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

# Try CORS proxies to fetch the page
wallet = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
target_url = f'https://taostats.io/pro/portfolio/{wallet}'

cors_proxies = [
    'https://cors-anywhere.herokuapp.com/',
    'https://api.allorigins.win/get?url=',
    'https://corsproxy.io/?',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

print("Testing CORS proxies...")
for proxy in cors_proxies:
    try:
        url = proxy + target_url
        print(f"\nTrying: {proxy[:40]}...")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"  Status: {response.status_code}")
        print(f"  Content length: {len(response.text)}")
        
        if response.status_code == 200:
            # Check if we got actual content
            if 'subnet' in response.text.lower() or 'portfolio' in response.text.lower():
                print("  -> Got relevant content!")
                # Save for analysis
                with open(f'proxy_content_{proxy.split("//")[1].split(".")[0]}.html', 'w') as f:
                    f.write(response.text)
            else:
                print(f"  -> Preview: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")