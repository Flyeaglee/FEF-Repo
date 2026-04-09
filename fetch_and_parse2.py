
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

# Fetch the page content
url = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    
    content = response.text
    
    # Look for JSON data in script tags
    # Common patterns for data in modern web apps
    json_patterns = [
        r'window\.__INITIAL_STATE__\s*=\s*({.*?});?',
        r'window\.__DATA__\s*=\s*({.*?});?',
        r'"portfolio":\s*({.*?})\s*[,}]',
        r'"subnets":\s*(\[.*?\])\s*[,}]',
    ]
    
    print("\nSearching for JSON data patterns...")
    for pattern in json_patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            print(f"Found match with pattern: {pattern[:50]}...")
            print(f"Match length: {len(matches[0])}")
            try:
                data = json.loads(matches[0])
                print(f"Successfully parsed JSON! Keys: {list(data.keys())[:5] if isinstance(data, dict) else 'Not a dict'}")
            except:
                print("Could not parse as JSON, might be truncated")
            break
    
    # Look for specific text patterns
    print("\n\nSearching for subnet-related content...")
    subnet_matches = re.findall(r'subnet[^<]{0,100}', content, re.IGNORECASE)
    print(f"Found {len(subnet_matches)} subnet references")
    if subnet_matches:
        for i, match in enumerate(subnet_matches[:5]):
            print(f"  {i+1}. {match[:100]}")
    
    # Look for table structures
    table_matches = re.findall(r'<table[^>]*>(.*?)</table>', content, re.DOTALL | re.IGNORECASE)
    print(f"\nFound {len(table_matches)} tables")
    
    # Look for data in specific format
    if 'data-reactroot' in content or 'data-reactid' in content:
        print("Page uses React")
    if '__NEXT_DATA__' in content:
        print("Page uses Next.js")
        # Extract Next.js data
        next_data_match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', content, re.DOTALL)
        if next_data_match:
            print("Found __NEXT_DATA__ script")
            try:
                next_data = json.loads(next_data_match.group(1))
                print(f"Next.js data keys: {list(next_data.keys())}")
                if 'props' in next_data:
                    print(f"Props keys: {list(next_data['props'].keys())}")
            except Exception as e:
                print(f"Error parsing Next.js data: {e}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()