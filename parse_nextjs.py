
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
import re
import json

url = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
content = response.text

# Look for __NEXT_DATA__
next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content, re.DOTALL)
if next_data_match:
    print("Found __NEXT_DATA__ script")
    try:
        next_data = json.loads(next_data_match.group(1))
        print(f"Top-level keys: {list(next_data.keys())}")
        
        if 'props' in next_data:
            props = next_data['props']
            print(f"\nProps keys: {list(props.keys())}")
            
            if 'pageProps' in props:
                page_props = props['pageProps']
                print(f"\nPageProps keys: {list(page_props.keys())}")
                
                # Look for portfolio or subnet data
                for key in page_props.keys():
                    print(f"\n--- Checking key: {key} ---")
                    value = page_props[key]
                    if isinstance(value, (dict, list)):
                        print(f"Type: {type(value).__name__}, Length: {len(value) if hasattr(value, '__len__') else 'N/A'}")
                        if isinstance(value, dict):
                            print(f"Sub-keys: {list(value.keys())[:10]}")
                        elif isinstance(value, list) and len(value) > 0:
                            print(f"First item type: {type(value[0]).__name__}")
                            if isinstance(value[0], dict):
                                print(f"First item keys: {list(value[0].keys())}")
                    else:
                        print(f"Value: {str(value)[:100]}")
                        
    except Exception as e:
        print(f"Error parsing: {e}")
        import traceback
        traceback.print_exc()
else:
    print("No __NEXT_DATA__ found")