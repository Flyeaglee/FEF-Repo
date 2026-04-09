
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
    content = response.text
    
    # Extract the large script tag
    script_pattern = r'<script[^>]*>(.*?)</script>'
    scripts = re.findall(script_pattern, content, re.DOTALL)
    
    # Find the largest script
    largest_script = max(scripts, key=len)
    print(f"Largest script size: {len(largest_script)}")
    
    # Look for specific patterns in the script
    # The data might be in a self-executing function or similar
    
    # Try to find JSON arrays that look like subnet data
    # Look for patterns like [{...}, {...}, ...]
    array_pattern = r'\[\s*\{[^\[\]]{100,5000}\}\s*\]'
    arrays = re.findall(array_pattern, largest_script, re.DOTALL)
    print(f"Found {len(arrays)} potential JSON arrays")
    
    for i, arr_str in enumerate(arrays[:5]):
        try:
            arr = json.loads(arr_str)
            if isinstance(arr, list) and len(arr) > 0:
                print(f"\nArray {i+1}: {len(arr)} items")
                if isinstance(arr[0], dict):
                    keys = list(arr[0].keys())
                    print(f"  Keys: {keys}")
                    # Check if this looks like subnet data
                    if any(k in keys for k in ['id', 'name', 'price', 'emission', 'subnet']):
                        print("  This looks like subnet data!")
                        # Save this data
                        print(f"  Sample item: {arr[0]}")
                        break
        except Exception as e:
            print(f"  Failed to parse array {i+1}: {str(e)[:50]}")
            continue
    
    # Also try looking for the specific structure
    # Look for "subnets" or similar keys
    subnet_key_pattern = r'"subnets"\s*:\s*(\[[^\[\]]{100,10000}\])'
    subnet_matches = re.findall(subnet_key_pattern, largest_script, re.DOTALL)
    print(f"\nFound {len(subnet_matches)} 'subnets' key matches")
    
    for i, match in enumerate(subnet_matches[:3]):
        try:
            arr = json.loads(match)
            print(f"Subnets array {i+1}: {len(arr)} items")
            if len(arr) > 0 and isinstance(arr[0], dict):
                print(f"  Keys: {list(arr[0].keys())}")
                print(f"  Sample: {arr[0]}")
        except Exception as e:
            print(f"  Failed: {str(e)[:50]}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()