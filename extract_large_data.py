
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
    
    # Extract the large script tag that likely contains all data
    script_pattern = r'<script[^>]*>(.*?)</script>'
    scripts = re.findall(script_pattern, content, re.DOTALL)
    
    # Find the largest script with subnet data
    largest_script = ""
    largest_size = 0
    
    for i, script in enumerate(scripts):
        if len(script) > 100000 and 'subnet' in script.lower():
            if len(script) > largest_size:
                largest_size = len(script)
                largest_script = script
    
    if largest_script:
        print(f"Found large script with subnet data (size: {len(largest_script)})")
        
        # Try to extract JSON data from this script
        # Look for common patterns where data is assigned to variables
        patterns = [
            r'\w+\s*=\s*({.*?});?\s*(?=var|const|let|function|</script>)',
            r'\w+\s*=\s*(\[.*?\]);?\s*(?=var|const|let|function|</script>)',
            r'data:\s*({.*?})\s*,\s*\w+',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, largest_script, re.DOTALL)
            print(f"Pattern '{pattern}' found {len(matches)} matches")
            
            for j, match in enumerate(matches[:3]):
                try:
                    # Clean up the match
                    clean_match = match.strip()
                    if clean_match.startswith("var ") or clean_match.startswith("const ") or clean_match.startswith("let "):
                        clean_match = clean_match.split("=", 1)[1].strip()
                    if clean_match.endswith(";"):
                        clean_match = clean_match[:-1].strip()
                        
                    data = json.loads(clean_match)
                    print(f"Successfully parsed JSON from match {j+1}")
                    
                    if isinstance(data, list):
                        print(f"Found list with {len(data)} items")
                        if len(data) > 0 and isinstance(data[0], dict):
                            print(f"Sample item keys: {list(data[0].keys())}")
                            # This is likely our subnet data
                            print("This looks like subnet data!")
                            break
                    elif isinstance(data, dict):
                        print(f"Found dict with keys: {list(data.keys())}")
                        # Look for nested arrays that might contain subnet data
                        for key, value in data.items():
                            if isinstance(value, list) and len(value) > 0:
                                print(f"List field '{key}' with {len(value)} items")
                                if isinstance(value[0], dict):
                                    print(f"Sample item keys: {list(value[0].keys())}")
                                    # This might be our subnet data
                                    print("This looks like subnet data!")
                                    break
                except Exception as e:
                    print(f"Failed to parse match {j+1}: {str(e)[:50]}")
                    continue
    else:
        print("No large script with subnet data found")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()