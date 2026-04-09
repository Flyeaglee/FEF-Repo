
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
import pandas as pd

# Test accessing taostats subnets data with more detailed parsing
url = 'https://taostats.io/subnets'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

try:
    response = requests.get(url, headers=headers, timeout=20)
    print(f"Status: {response.status_code}")
    content = response.text
    
    # Look for the main subnet data JSON structure
    # Try to find a large JSON object that likely contains subnet data
    json_matches = re.findall(r'\{[^{}]{1000,10000}\}', content)
    print(f"Found {len(json_matches)} large JSON objects")
    
    # Look for subnet-related data
    subnet_data = []
    for i, match in enumerate(json_matches[:10]):
        try:
            data = json.loads(match)
            # Check if this looks like subnet data
            if isinstance(data, dict):
                # Look for common subnet fields
                str_data = str(data).lower()
                if any(keyword in str_data for keyword in ['subnet', 'name', 'id', 'price', 'emission']):
                    print(f"Potential subnet data found in JSON {i+1}")
                    print(f"Data keys sample: {str(list(data.keys())[:10]) if isinstance(data, dict) else 'N/A'}")
                    # Try to extract subnet information
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, list) and len(value) > 0:
                                print(f"List field '{key}' with {len(value)} items")
                                if isinstance(value[0], dict):
                                    print(f"  Sample item keys: {list(value[0].keys())[:5]}")
                                    # This might be our subnet data
                                    subnet_data = value
                                    break
                        if subnet_data:
                            break
        except Exception as e:
            continue
    
    if subnet_data:
        print(f"\nFound {len(subnet_data)} subnet records")
        # Display first few records
        for i, subnet in enumerate(subnet_data[:3]):
            print(f"\nSubnet {i+1}: {subnet}")
    else:
        print("No subnet data found in JSON structures")
        
        # Try alternative approach - look for table-like data
        print("\nTrying alternative parsing approach...")
        # Look for table rows or structured data
        table_pattern = r'<tr[^>]*>.*?</tr>'
        table_rows = re.findall(table_pattern, content, re.DOTALL)
        print(f"Found {len(table_rows)} table rows")
        if table_rows:
            for i, row in enumerate(table_rows[:5]):
                if 'subnet' in row.lower() or 'price' in row.lower():
                    print(f"Row {i+1}: {row[:200]}")
                    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()