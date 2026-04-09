
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


# Test the proxy server logic directly
import requests
import re

WALLET_ADDRESS = '5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'

def fetch_taostats_data():
    """Fetch portfolio data from taostats.io"""
    url = f'https://taostats.io/pro/portfolio/{WALLET_ADDRESS}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        print(f"Fetching from: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Response status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check if we got redirected to login
            if 'login' in content.lower() and 'redirect' in content.lower():
                print("Page requires authentication (redirected to login)")
                return {
                    'success': False,
                    'requiresAuth': True,
                    'error': 'Portfolio data requires authentication'
                }
            
            # Try to extract data
            print("\nSearching for data patterns...")
            
            # Look for JSON in scripts
            json_patterns = [
                r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
                r'window\.__INITIAL_STATE__\s*=\s*({.*?});?',
            ]
            
            for pattern in json_patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    print(f"Found pattern: {pattern[:40]}...")
                    try:
                        data = json.loads(match.group(1))
                        print(f"JSON parsed successfully! Keys: {list(data.keys())[:5] if isinstance(data, dict) else 'N/A'}")
                        return {
                            'success': True,
                            'data': data,
                            'source': 'taostats.io'
                        }
                    except Exception as e:
                        print(f"Failed to parse JSON: {e}")
            
            return {
                'success': False,
                'requiresAuth': True,
                'error': 'Could not extract data from page'
            }
        else:
            return {
                'success': False,
                'error': f'HTTP {response.status_code}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Test the function
print("Testing taostats data fetch...")
result = fetch_taostats_data()
print(f"\nResult: {result}")