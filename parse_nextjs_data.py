
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
import re

# Try using a CORS proxy to access taostats API
proxy = 'https://api.codetabs.com/v1/proxy?quest='
url = proxy + 'https://taostats.io/subnets'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    print(f"Status: {response.status_code}")
    content = response.text
    print(f"Content length: {len(content)}")
    
    # Look for script tags with JSON data
    script_pattern = r'<script[^>]*>(.*?)</script>'
    scripts = re.findall(script_pattern, content, re.DOTALL)
    print(f"Found {len(scripts)} script tags")
    
    # Look for JSON in scripts
    for i, script in enumerate(scripts):
        if len(script) > 500 and ('subnet' in script.lower() or 'price' in script.lower() or 'emission' in script.lower()):
            print(f"\nScript {i+1} contains relevant data (length: {len(script)})")
            # Try to find JSON objects in the script
            json_matches = re.findall(r'\{[^{}]{100,5000}\}', script)
            for j, match in enumerate(json_matches[:3]):
                try:
                    data = json.loads(match)
                    if isinstance(data, dict):
                        str_data = str(data).lower()
                        if any(keyword in str_data for keyword in ['subnet', 'name', 'id', 'price', 'emission', 'tao']):
                            print(f"  JSON {j+1} keys: {list(data.keys())[:10]}")
                            # Check if this is an array of subnets
                            for key, value in data.items():
                                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                                    print(f"  Found list '{key}' with {len(value)} items")
                                    print(f"  Sample item: {value[0]}")
                                    break
                except:
                    pass
                    
    # Also look for __NEXT_DATA__ which is common in Next.js apps
    next_data_pattern = r'window\.__NEXT_DATA__\s*=\s*({.*?});?\s*</script>'
    next_data_match = re.search(next_data_pattern, content, re.DOTALL)
    if next_data_match:
        print("\nFound __NEXT_DATA__")
        try:
            next_data = json.loads(next_data_match.group(1))
            print(f"Keys: {list(next_data.keys())[:10]}")
            if 'props' in next_data:
                props = next_data['props']
                print(f"Props keys: {list(props.keys())[:10]}")
                if 'pageProps' in props:
                    page_props = props['pageProps']
                    print(f"PageProps keys: {list(page_props.keys())[:10]}")
        except Exception as e:
            print(f"Error parsing __NEXT_DATA__: {e}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()