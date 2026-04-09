
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
from bs4 import BeautifulSoup

# Fetch the page content
url = 'https://taostats.io/pro/portfolio/5CEhmdqho1Rnfri4W8KyF8nqkiovB9YQQDtH9pvFWpE3ndzZ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    
    # Save the HTML to analyze it
    with open('taostats_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for tables or data structures
    tables = soup.find_all('table')
    print(f"\nFound {len(tables)} tables")
    
    # Look for subnet-related content
    if 'subnet' in response.text.lower():
        print("Found 'subnet' in page content")
    
    # Look for specific data patterns
    if 'TAO' in response.text:
        print("Found 'TAO' in page content")
    
    # Try to find data in script tags (might be JSON data)
    scripts = soup.find_all('script')
    print(f"\nFound {len(scripts)} script tags")
    
    # Look for JSON data in scripts
    for i, script in enumerate(scripts):
        if script.string and len(script.string) > 100:
            if 'portfolio' in script.string.lower() or 'subnet' in script.string.lower():
                print(f"\nScript {i} might contain data (length: {len(script.string)})")
                print(script.string[:500])
                break
    
    # Look for specific elements that might contain subnet data
    print("\n\nLooking for subnet data in page...")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()